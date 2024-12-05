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
"""Concurrency and support of same.

Objects and classes that allow for the construction of
complex distributed operations.
"""
__docformat__ = 'restructuredtext'

import ansar.encode as ar
from .lifecycle import *
from .point import *
from .machine import *

__all__ = [
	'CreateFrame',
	'GetResponse',
	'Concurrently',
	'Sequentially',
]

#
class CreateFrame(object):
	"""Capture values needed for async object creation.

	:param object_type: type to be created
	:type object_type: function or Point-based class
	:param args: positional parameters
	:type args: tuple
	:param kw: named parameters
	:type kw: dict
	"""
	def __init__(self, object_type, *args, **kw):
		self.object_type = object_type
		self.args = args
		self.kw = kw

#
class GetResponse(Point, Stateless):
	"""Object to that sends request and returns response as completion."""
	def __init__(self, request, server_address, seconds=None):
		Point.__init__(self)
		Stateless.__init__(self)
		self.request = request
		self.server_address = server_address
		self.seconds = seconds

def GetResponse_Start(self, message):
	self.send(self.request, self.server_address)	# Request.
	if self.seconds is not None:
		self.start(T1, self.seconds)

def GetResponse_T1(self, message):						# Too slow.
	self.complete(TimedOut(message))

def GetResponse_Stop(self, message):					# Interruption.
	self.complete(Aborted())

def GetResponse_Unknown(self, message):	# Assumed to be response. Use as completion.
	self.complete(message)

GET_RESPONSE_DISPATCH = [
	Start,
	T1,
	Stop,
	ar.Unknown,
]

bind_stateless(GetResponse, GET_RESPONSE_DISPATCH, thread='get-response')

#
class Concurrently(Point, Stateless):
	"""Object that initiates multiple objects and produces list of completions."""
	def __init__(self, *get, seconds=None):
		Point.__init__(self)
		Stateless.__init__(self)
		self.get = get		# List of object descriptions.
		self.count = len(get)		# Save for countdown.
		self.seconds = seconds
		self.orderly = [None] * self.count	# Prepare the completion list.

def Concurrently_Start(self, message):
	if self.count < 1:
		self.complete(self.orderly)		# Nothing to do.

	def collate(response, i):			# Place the completion in its proper slot.
		self.orderly[i] = response
		self.count -= 1
		if self.count < 1:
			self.complete(self.orderly)

	# Create an object for each slot. Allow full object spec
	# or the request-address tuple.
	for i, p in enumerate(self.get):
		if isinstance(p, CreateFrame):
			a = self.create(p.object_type, *p.args,	**p.kw)
		elif isinstance(p, tuple) and len(p) == 2:
			r, s = p
			a = self.create(GetResponse, r, s)		# Provide the object for simple request-response exchange.
		else:
			self.complete(ar.Faulted(f'unexpected collective item [{i}]'))

		self.assign(a, OnCompleted(collate, i))

	if self.seconds is not None:
		self.start(T1, self.seconds)

def Concurrently_T1(self, message):
	self.abort(TimedOut(message))

def Concurrently_Stop(self, message):
	self.abort(Aborted())

def Concurrently_Completed(self, message):
	d = self.debrief()
	if isinstance(d, OnCompleted):
		d(message.value)
		return
	
	self.complete(ar.Faulted(f'unexpected get completion'))

COLLECTIVELY_DISPATCH = [
	Start,
	Completed,
	T1,
	Stop,
]

bind_stateless(Concurrently, COLLECTIVELY_DISPATCH, thread='concurrently')


#
class Sequentially(Point, Stateless):
	"""Object that iterates multiple objects and produces list of completions."""
	def __init__(self, *get, seconds=None):
		Point.__init__(self)
		Stateless.__init__(self)
		self.get = get
		self.pointer = iter(self.get)
		self.seconds = seconds
		self.orderly = []

	def next_step(self):
		try:
			p = next(self.pointer)
		except StopIteration:
			self.complete(self.orderly)

		if isinstance(p, CreateFrame):
			a = self.create(p.object_type, *p.args,	**p.kw)
		elif isinstance(p, tuple) and len(p) == 2:
			r, s = p
			a = self.create(GetResponse, r, s)		# Provide the object for simple request-response exchange.
		else:
			i = len(self.orderly)
			self.complete(ar.Faulted(f'unexpected sequence item [{i}]'))
		return a

def Sequentially_Start(self, message):
	def begin():
		a = self.next_step()
		self.then(a, step)

	def step(value):
		if isinstance(value, ar.Faulted):
			self.complete(value)
		self.orderly.append(value)

		a = self.next_step()
		self.then(a, step)

	if self.seconds is not None:
		self.start(T1, self.seconds)

	begin()

def Sequentially_T1(self, message):
	self.abort(TimedOut(message))

def Sequentially_Stop(self, message):
	self.abort(Aborted())

def Sequentially_Completed(self, message):
	d = self.debrief()
	if isinstance(d, OnCompleted):
		d(message.value)
		return

	self.complete(ar.Faulted(f'unexpected sequence completion'))

SEQUENTIALLY_DISPATCH = [
	Start,
	T1,
	Stop,
	Completed,
]

bind_stateless(Sequentially, SEQUENTIALLY_DISPATCH, thread='sequentially')
