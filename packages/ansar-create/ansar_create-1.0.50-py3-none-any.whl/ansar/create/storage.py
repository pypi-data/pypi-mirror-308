# Author: Scott Woods <scott.18.ansar@gmail.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Movement of files to home processes and back.

"""
__docformat__ = 'restructuredtext'

import os
import stat
#import pwd
#import grp
import uuid
import shutil
import datetime

__all__ = [
	'DELTA_FILE_ADD', 'DELTA_FILE_UPDATE', 'DELTA_FILE_UGM', 'DELTA_FILE_REMOVE',
	'DELTA_FOLDER_ADD', 'DELTA_FOLDER_UPDATE', 'DELTA_FOLDER_UGM', 'DELTA_FOLDER_REMOVE',
	'DELTA_FILE_CRUD', 'DELTA_FOLDER_CRUD',
	'DELTA_CRUD',
	'StorageTables',
	'StorageAttributes',
	'StorageManifest',
	'StorageListing',
	'StorageTables',
	'storage_manifest',
	'storage_walk',
	'storage_delta',
	'DeltaMachine',
	'RemoveFolder',
	'RemoveFile',
	'UpdateFile',
	'UpdateUser',
	'UpdateGroup',
	'UpdateMode',
	'AddFile',
	'AddFolder',
	'ReplaceWithFile',
	'ReplaceWithFile',
]

#
#
import ansar.encode as ar

# User, group ids and mode (permissions - rwxrwxrwx).
#
class StorageAttributes(object):
	"""Attributes of a folder/file in a storage hierarchy."""
	def __init__(self, user=None, group=None, mode=None):
		self.user = user
		self.group = group
		self.mode = mode

	def __str__(self):
	#	user = pwd.getpwuid(self.user)
	#	group = grp.getgrgid(self.group)
	#	rwx = stat.filemode(self.mode)
	#	return f'StorageAttributes(owner={user.pw_name}, group={group.gr_name}, permissions={rwx})'
		return f'StorageAttributes(owner={self.user}, group={self.group}, permissions={self.mode})'


STORAGE_ATTRIBUTES_SCHEMA = {
	'user': int,
	'group': int,
	'mode': int,
}

ar.bind(StorageAttributes, object_schema=STORAGE_ATTRIBUTES_SCHEMA, copy_before_sending=False)

#
#
class StorageManifest(object):
	"""Folder in a folder/file storage hierarchy."""
	def __init__(self, path=None, modified=None, attributes=None, content=None, parent=None, manifests=0, listings=0, bytes=0):
		self.path = path
		self.modified = modified
		self.attributes = attributes or StorageAttributes()
		self.content = content or ar.default_map()
		self.parent = parent
		self.manifests = manifests
		self.listings = listings
		self.bytes = bytes

	def full_path(self):
		return self.path

	def origin(self):
		if self.parent is None:
			return self.path
		return self.parent.origin()

	def __str__(self):
		return f'StorageManifest(path={self.path}, modified={self.modified}, attributes={self.attributes}, contents={len(self.content)})'


STORAGE_MANIFEST_SCHEMA = {
	'path': str,
	'modified': ar.WorldTime(),
	'attributes': ar.UserDefined(StorageAttributes),
	'content': ar.MapOf(str, ar.Any()),
	'parent': ar.PointerTo(StorageManifest),
	'manifests': int,
	'listings': int,
	'bytes': int,
}

ar.bind(StorageManifest, object_schema=STORAGE_MANIFEST_SCHEMA, copy_before_sending=False)

#
#
class StorageListing(object):
	"""File in a folder/file storage hierarchy."""
	def __init__(self, name=None, modified=None, attributes=None, size=0, parent=None):
		self.name = name
		self.modified = modified
		self.attributes = attributes or StorageAttributes()
		self.size = size
		self.parent = parent

	def full_path(self):
		p = os.path.join(self.parent.path, self.name)
		return p

	def origin(self):
		return self.parent.origin()

	def __str__(self):
		return f'StorageListing(name={self.name}, modified={self.modified}, attributes={self.attributes})'

STORAGE_LISTING_SCHEMA = {
	'name': str,
	'modified': ar.WorldTime(),
	'attributes': ar.UserDefined(StorageAttributes),
	'size': int,
	'parent': ar.PointerTo(StorageManifest),
}

ar.bind(StorageListing, object_schema=STORAGE_LISTING_SCHEMA, copy_before_sending=False)

#
#
class StorageTables(object):
	"""Names for ids appearing in a folder/file hierarchy."""
	def __init__(self, user_name=None, group_name=None):
		self.user_name = user_name or ar.default_map()
		self.group_name = group_name or ar.default_map()

	def __str__(self):
		return f'StorageTables(user_name={len(self.user_name)}, group_name={len(self.group_name)})'

STORAGE_TABLES_SCHEMA = {
	'user_name': ar.MapOf(int, str),
	'group_name': ar.MapOf(int, str),
}

ar.bind(StorageTables, object_schema=STORAGE_TABLES_SCHEMA, copy_before_sending=False)

#
#
def storage_manifest(path, parent=None, table=None):
	"""Scan the given folder, recursively. Return a manifest of contents."""
	table = table or StorageTables()
	user_name = table.user_name
	group_name = table.group_name

	# Small optimization to reduce hits on the
	# platform dbs.
	def lookup(s):
		# User ids <---> names
		try:
			t = user_name[s.st_uid]	 # Already seen?
		except KeyError:
			t = None				# Not defined.
			#try:
			#	t = pwd.getpwuid(s.st_uid).pw_name	# Nope - lookup.
			#except KeyError:
			#	t = None				# Not defined.
			user_name[s.st_uid] = t	 # Remember results.
		# Group ids <---> names
		try:
			t = group_name[s.st_gid]
		except KeyError:
			t = None
			#try:
			#	t = grp.getgrgid(s.st_gid).gr_name
			#except KeyError:
			#	t = None
			group_name[s.st_gid] = t
		a = StorageAttributes(user=s.st_uid, group=s.st_gid, mode=s.st_mode)
		return a

	s = os.stat(path)
	d = datetime.datetime.fromtimestamp(s.st_mtime, tz=ar.UTC)
	a = lookup(s)
	m = StorageManifest(path=path, modified=d, attributes=a, parent=parent)

	content = m.content
	for k in os.listdir(path):
		p = os.path.join(path, k)
		if os.path.isdir(p):
			m.manifests += 1
			v, _ = storage_manifest(p, parent=m, table=table)
			m.manifests += v.manifests
			m.listings += v.listings
			m.bytes += v.bytes
		elif os.path.isfile(p):
			m.listings += 1
			s = os.stat(p)
			d = datetime.datetime.fromtimestamp(s.st_mtime, tz=ar.UTC)
			a = lookup(s)
			v = StorageListing(name=k, modified=d, attributes=a, size=s.st_size, parent=m)
			m.bytes += v.size
		else:
			continue
		content[k] = v

	return m, table

# Flatten the hierarchy into a list
# of full name and manifest/listing.
def storage_walk(man):
	for k, v in man.content.items():
		if isinstance(v, StorageManifest):
			yield from storage_walk(v)
		elif isinstance(v, StorageListing):
			yield v.full_path(), v
	yield man.path, man

# Printing of a storage area.
#
def show_file(header, listing):
	print('%s- %s (%d)' % (header, listing.name, listing.size))

def show_folder(header, manifest):
	p, f = os.path.split(manifest.path)
	print('%s+ %s (%d, %d, %d)' % (header, f, manifest.manifests, manifest.listings, manifest.bytes))

def show_listings(man):
	path, name = os.path.split(man.path)
	c = len(path) + 1

	d = {k[c:]: v for k, v in storage_walk(man)}
	s = sorted(d)
	for p in s:
		v = d[p]
		t = p.split(os.path.sep)
		n = len(t)
		if n == 1:
			print('%s (%d, %d, %d)' % (man.path, man.manifests, man.listings, man.bytes))
		elif isinstance(v, StorageManifest):
			h = '  ' * (n - 2)
			show_folder(h, v)
		else:
			h = '  ' * (n - 2)
			show_file(h, v)

class TransferHalted(Exception):
	pass

DELTA_FILE_ADD = 0x01
DELTA_FILE_UPDATE = 0x02
DELTA_FILE_UGM = 0x04
DELTA_FILE_REMOVE = 0x08
DELTA_FILE_CRUD = DELTA_FILE_ADD | DELTA_FILE_UPDATE | DELTA_FILE_UGM | DELTA_FILE_REMOVE

DELTA_FOLDER_ADD = 0x10
DELTA_FOLDER_UPDATE = 0x20		# Walk down into sub-folders.
DELTA_FOLDER_UGM = 0x40
DELTA_FOLDER_REMOVE = 0x80
DELTA_FOLDER_CRUD = DELTA_FOLDER_ADD | DELTA_FOLDER_UPDATE | DELTA_FOLDER_UGM | DELTA_FOLDER_REMOVE

DELTA_CRUD = DELTA_FILE_CRUD | DELTA_FOLDER_CRUD

class DeltaMachine(object):
	def __init__(self, context, target):
		self.context = context
		self.target = target
		self.alias_file = {}
		self.alias_folder = {}

	# Map a source to its final target.
	def resting(self, ml):
		origin = ml.origin()	  # Location of source.
		path = ml.full_path()		# Full path and name.
		len_origin = len(origin)

		source, name = os.path.split(path)  # Clip name off.
		if len_origin == len(source):
			t = os.path.join(self.target, name)	# No relative component.
		else:
			t = os.path.join(self.target, source[len_origin + 1:], name)
		return t

	def alias(self, d, m):
		s = str(uuid.uuid4())		   # Actual alias.
		origin = d.source.origin()	  # Location of source.
		len_origin = len(origin)

		path = d.source.full_path()
		source, _ = os.path.split(path)  # Clip name off.
		# Want to replace the source location with the target
		# location and the final name with the alias name.
		# Extra detail is including the relative path, if any.
		if len_origin == len(source):
			t = os.path.join(self.target, s)	# No relative component.
		else:
			t = os.path.join(self.target, source[len_origin + 1:], s)
		m[path] = t
		return t

	def aliases(self):
		a = len(self.alias_file) + len(self.alias_folder)
		return a

	def rename(self):
		for k, a in self.alias_file.items():
			#if self.halted:
			#	return ar.Aborted()
			p, _ = os.path.split(a)
			_, t = os.path.split(k)
			e = os.path.join(p, t)
			os.rename(a, e)
		self.alias_file = {}
		for k, a in self.alias_folder.items():
			#if self.halted:
			#	return ar.Aborted()
			p, _ = os.path.split(a)
			_, t = os.path.split(k)
			e = os.path.join(p, t)
			os.rename(a, e)
		self.alias_folder = {}

	def clear(self):
		"""Clean up any transfer artefacts."""
		for _, v in self.alias_file.items():
			try:
				os.remove(v)
			except FileNotFoundError:
				pass

		for _, v in self.alias_folder.items():
			try:
				ar.remove_folder(v)
			except ar.FileNotFound:
				pass

# Actual file and folder copying fragements.
def transfer_file(self, source, target):
	"""Copy a single executable to an interim alias."""
	with open(source, 'rb') as r, open(target, 'wb') as w:
		while True:
			if self.halted:
				raise TransferHalted()
			t = r.read(4096)
			if t == b'':
				break
			w.write(t)
	shutil.copystat(source, target)

def add_folder(self, source, target):
	"""Add folder cos folders are never transferred, i.e. like a file update."""
	try:
		os.makedirs(target)
		shutil.copystat(source, target)
	except FileExistsError:		# Might be hiding a bug with this.
		pass
	# Loop through contents, as defined by the
	# source folder.
	for f in os.listdir(source):
		if self.halted:
			raise TransferHalted()
		s = os.path.join(source, f)
		t = os.path.join(target, f)
		if os.path.isdir(s):
			add_folder(self, s, t)
		elif os.path.isfile(s):
			transfer_file(self, s, t)

#
#
class RemoveFolder(object):
	def __init__(self, folder=None):
		self.folder = folder

	def __str__(self):
		return f'RemoveFolder(path={self.folder.path}, modified={self.folder.modified}, contents={len(self.folder.content)})'

	def __call__(self, dm):
		p = self.folder.path
		ar.remove_folder(p)

REMOVE_FOLDER_SCHEMA = {
	'folder': ar.PointerTo(StorageManifest),
}

class RemoveFile(object):
	def __init__(self, file=None):
		self.file = file

	def __str__(self):
		return f'RemoveFile(path={self.file.full_path()}, modified={self.file.modified})'

	def __call__(self, dm):
		f = self.file.full_path()
		os.remove(f)

REMOVE_FILE_SCHEMA = {
	'file': ar.PointerTo(StorageListing),
}

class UpdateFile(object):
	def __init__(self, source=None, target=None):
		self.source = source
		self.target = target

	def __str__(self):
		return f'UpdateFile(path={self.source.full_path()}, modified={self.source.modified}, target={self.target.parent.path})'

	def __call__(self, dm):
		a = dm.alias(self, dm.alias_file)
		transfer_file(dm.context, self.source.full_path(), a)

UPDATE_FILE_SCHEMA = {
	'source': ar.PointerTo(StorageListing),
	'target': ar.PointerTo(StorageListing),
}

class UpdateUser(object):
	def __init__(self, target=None, user=None):
		self.target = target
		self.user = user

	def __str__(self):
		return f'UpdateUser(target={self.target.full_path()}, user={self.user})'

	def __call__(self, dm):
		pass

UPDATE_USER_SCHEMA = {
	'target': ar.PointerTo(ar.Any()),
	'user': int,
}

class UpdateGroup(object):
	def __init__(self, target=None, group=None):
		self.target = target
		self.group = group

	def __str__(self):
		return f'UpdateGroup(target={self.target.full_path()}, group={self.group})'

	def __call__(self, dm):
		pass

UPDATE_GROUP_SCHEMA = {
	'target': ar.PointerTo(ar.Any()),
	'group': int,
}

class UpdateMode(object):
	def __init__(self, target=None, mode=None):
		self.target = target
		self.mode = mode

	def __str__(self):
		return f'UpdateMode(target={self.target.full_path()}, mode={self.mode})'

	def __call__(self, dm):
		f = self.target.full_path()
		os.chmod(f, self.mode)

UPDATE_MODE_SCHEMA = {
	'target': ar.PointerTo(ar.Any()),
	'mode': int,
}

class AddFile(object):
	def __init__(self, source=None, target=None):
		self.source = source
		self.target = target

	def __str__(self):
		return f'AddFile(path={self.source.full_path()}, target={self.target.path})'

	def __call__(self, dm):
		a = dm.alias(self, dm.alias_file)
		transfer_file(dm.context, self.source.full_path(), a)

ADD_FILE_SCHEMA = {
	'source': ar.PointerTo(StorageListing),
	'target': ar.PointerTo(StorageManifest),
}

class AddFolder(object):
	def __init__(self, source=None, target=None):
		self.source = source
		self.target = target

	def __str__(self):
		return f'AddFolder(path={self.source.path}, target={self.target.path})'

	def __call__(self, dm):
		a = dm.alias(self, dm.alias_folder)
		add_folder(dm.context, self.source.path, a)

ADD_FOLDER_SCHEMA = {
	'source': ar.PointerTo(StorageManifest),
	'target': ar.PointerTo(StorageManifest),
}

class ReplaceWithFile(object):
	def __init__(self, source=None, target=None):
		self.source = source
		self.target = target

	def __str__(self):
		return f'ReplaceWithFile(source={self.source.full_path()}, target={self.target.path})'

	def __call__(self, dm):
		p = self.target.path
		ar.remove_folder(p)
		a = dm.alias(self, dm.alias_file)
		transfer_file(dm.context, self.source.full_path(), a)

REPLACE_WITH_FILE_SCHEMA = {
	'source': ar.PointerTo(StorageListing),
	'target': ar.PointerTo(StorageManifest),
}

class ReplaceWithFolder(object):
	def __init__(self, source=None, target=None):
		self.source = source
		self.target = target

	def __str__(self):
		return f'ReplaceWithFolder(path={self.source.path}, target={self.target.full_path()})'

	def __call__(self, dm):
		f = self.target.full_path()
		os.remove(f)
		a = dm.alias(self, dm.alias_folder)
		add_folder(self, self.source.path, a)

REPLACE_WITH_FOLDER_SCHEMA = {
	'source': ar.PointerTo(StorageManifest),
	'target': ar.PointerTo(StorageListing),
}

ar.bind(RemoveFolder, object_schema=REMOVE_FOLDER_SCHEMA)
ar.bind(RemoveFile, object_schema=REMOVE_FILE_SCHEMA)
ar.bind(UpdateFile, object_schema=UPDATE_FILE_SCHEMA)
ar.bind(UpdateUser, object_schema=UPDATE_USER_SCHEMA)
ar.bind(UpdateGroup, object_schema=UPDATE_GROUP_SCHEMA)
ar.bind(UpdateMode, object_schema=UPDATE_MODE_SCHEMA)
ar.bind(AddFile, object_schema=ADD_FILE_SCHEMA)
ar.bind(AddFolder, object_schema=ADD_FOLDER_SCHEMA)
ar.bind(ReplaceWithFolder, object_schema=REPLACE_WITH_FOLDER_SCHEMA)
ar.bind(ReplaceWithFile, object_schema=REPLACE_WITH_FILE_SCHEMA)

def storage_delta(source, target, flags=DELTA_CRUD):
	"""Compare the two trees. Yield a sequence of the changes needed."""
	def content_keys(m):
		if m is None:
			return []
		return m.content.keys()
	keys = content_keys(source) | content_keys(target)

	# Source and target guaranteed to exist and represent the
	# equivalent nodes (i.e. manifests) of their respective trees.
	# Iterate through this pair of nodes using the union of the two
	# sets of keys.

	for k in keys:
		s = None if source is None else source.content.get(k, None)
		t = None if target is None else target.content.get(k, None)
		# Possibilities are;
		# s, t ...... compare
		# s, None ... add
		# None, t ... remove
		# (Note: None, None never happens)
		if s:
			if t:
				# At equivalent sub-nodes in the tree.
				# Could be 2 folders or 2 files, or
				# mismatched folder and file.
				if type(s) == type(t):
					if isinstance(s, StorageManifest):
						if flags & DELTA_FOLDER_UPDATE: yield from storage_delta(s, t, flags=flags)			# Recurse.
						if s.attributes.user != t.attributes.user and flags & DELTA_FOLDER_UGM:
							yield UpdateUser(t, s.attributes.user)
						if s.attributes.group != t.attributes.group and flags & DELTA_FOLDER_UGM:
							yield UpdateGroup(t, s.attributes.group)
						if s.attributes.mode != t.attributes.mode and flags & DELTA_FOLDER_UGM:
							yield UpdateMode(t, s.attributes.mode)
					else:
						if s.modified > t.modified and flags & DELTA_FILE_UPDATE:
							yield UpdateFile(s, t)		# Creates new target file.
							continue
						if s.attributes.user != t.attributes.user and flags & DELTA_FILE_UGM:
							yield UpdateUser(t, s.attributes.user)
						if s.attributes.group != t.attributes.group and flags & DELTA_FILE_UGM:
							yield UpdateGroup(t, s.attributes.group)
						if s.attributes.mode != t.attributes.mode and flags & DELTA_FILE_UGM:
							yield UpdateMode(t, s.attributes.mode)
				elif type(s) == StorageManifest:
					if flags & DELTA_FILE_REMOVE and flags & DELTA_FOLDER_ADD: yield ReplaceWithFolder(s, t)
				else:
					if flags & DELTA_FOLDER_REMOVE and flags & DELTA_FILE_ADD: yield ReplaceWithFile(s, t)
			else:
				# No t - add file/folder
				if isinstance(s, StorageManifest):
					if flags & DELTA_FOLDER_ADD: yield AddFolder(s, target)
				else:
					if flags & DELTA_FILE_ADD: yield AddFile(s, target)
		else:
			# No s - trim from target
			if isinstance(t, StorageManifest):
				if flags & DELTA_FOLDER_REMOVE: yield RemoveFolder(t)
			else:
				if flags & DELTA_FILE_REMOVE: yield RemoveFile(t)

def storage_delta_removals(source, target):
	"""Compare the two manifests. Return the ops to update the target.

	The sequence is optimized to reduce the maximum storage required at the
	target end, i.e. all removals are performed first, then updates and lastly
	any additions. Folders that need to be added or removed only appear as
	the folder operations, i.e. objects under those folders do not appear
	in the list of operations.
	"""
	s, t = source.content.keys(), target.content.keys()

	add = s - t	   # In source only
	update = s & t	# Both
	remove = t - s	# Target only

	for r in remove:
		t = target.content[r]
		if isinstance(t, StorageManifest):
			yield RemoveFolder(t)
		else:
			yield RemoveFile(t)

	for c in update:
		s, t = source.content[c], target.content[c]
		if type(s) == type(t):
			if isinstance(s, StorageManifest):
				yield from storage_delta(s, t)
			elif s.modified > t.modified:
				yield UpdateFile(s, t)		# Creates new target file.
				continue
			if s.attributes.user != t.attributes.user:
				yield UpdateUser(t, s.attributes.user)
			if s.attributes.group != t.attributes.group:
				yield UpdateGroup(t, s.attributes.group)
			if s.attributes.mode != t.attributes.mode:
				yield UpdateMode(t, s.attributes.mode)
		elif type(s) == StorageManifest:
			yield RemoveFile(t)
			yield AddFolder(s, target)
		else:
			yield RemoveFolder(t)
			yield AddFile(s, target)

	for a in add:
		c = source.content[a]
		if isinstance(c, StorageManifest):
			yield AddFolder(c, target)
		else:
			yield AddFile(c, target)
