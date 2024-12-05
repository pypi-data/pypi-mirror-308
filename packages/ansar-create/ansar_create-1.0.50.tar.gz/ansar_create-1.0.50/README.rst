
ansar-create
============

The **ansar-create** library uses multi-threading and multi-processing to solve difficult
software challenges such as concurrency, interruption and cancellation. It wraps those
platform facilities in a standard runtime model, giving developers the ability to express
that type of software in a clear and consistent manner.

This type of software is often referred to as asynchronous, event-driven or reactive
software. It acknowledges the fundamental fact that significant events can occur at
any time, and that software must be able to respond to those events in a reliable
and timely manner.

Features
--------

- Based on a standard model for complex software operations (SDL)
- Uniform management of threads, processes and state machines
- Built-in runtime facilities such as timers and logging.
- Persistent application configuration.
- Process orchestration.
- Development automation.


Changelog
=========

1.0.18 (2024-09-09)
-------------------

- Upgrade of FSM processing - DEFAULT state and base class matching.

- Improved auto logging of timer activity

1.0 (2024-05-27)
----------------

- Implement objects and send

- Implement home and roles

- Implement ansar CLI

- Complete **ansar-create** docs
