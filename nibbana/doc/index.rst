=========
 Nibbana
=========

.. contents::
  :depth: 3

Installation
============
* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way.
* `Activate longpolling <https://odoo-development.readthedocs.io/en/latest/admin/longpolling.html>`__ to refresh tree view with tasks and projects.
* *Optional, but strongly recommended*. If you want color highlight install OCA modules `web_tree_dynamic_colored_field <https://apps.odoo.com/apps/modules/11.0/web_tree_dynamic_colored_field/>`__ and
  `web_widget_color <https://apps.odoo.com/apps/modules/11.0/web_widget_color//>`__.

Nibbana concepts
================
**What we focus are attention becomes our reality**

I am mad about productivity and effectiveness.
I was used to use Getting Things Done (GTD) by 
`David Allen <https://gettingthingsdone.com>`__ and Auto Focus methods by `Mark Forster <http://markforster.squarespace.com>`__ and could not 
find a software product to satisfy all I need. 
Everything what I tried was missing some part of the wholeness.
So I met Odoo and created Nibbana. 

User features
=============

* **GTD** implementation with energy and available time conditions. Inbox, Areas, 
  Contexts, Next, Waiting, Someday, Scheduled. 

* **Do it today / Do it tomorrow** by `Mark Forster <http://markforster.squarespace.com>`__.  Mix
  of GTD and these two technics makes possible the real juggling. 

* **Analitycs and metrics**. Odoo actually is a business platform with nice anaylitics features. 
  Metrics are recorded as you go with your projects and tasks so that you get a clear 
  picture of what you do and how you do.


What makes Nibbana different
============================

Here is the list of unique feature not present anywhere I know.

* **Nibbana** only seems to be a project & task management tool. In reality it is a tool that can help you balance your life. If you follow Nibbana's way of managing your  issues you will able to track your **Wheel of Life**.

* **Retro analisys**. Nibbana does not put your projects in the trash. It keeps it hidden from everywhere until you want to rewind. Looking back at the history of your days you can notice that some projects are coming from the very past and still make you worried about. These projects seem to be your karma :-) You can notice that you go round by round without success and suddenly undestand your blind spot  that made you not succeed. Nibbana gives you the ability to see your current projects and tasks after some time the same form as they look now. It's like your **time machine**.

* **Metrics**. Nibbana remembers how you use it. It gives your a visual representation of how active you are moving your projects and tasks along its life cycle. **If you start to procrastinate** Nibbana tries to wake you up. You can understand your limits. Also you can see the truth about youself.


Nibbana's way
=============

If you want to get all benefits from this software your should follow the path described below.

* **Be born every morning**. If you want to make the God laugh tell him about your plans. It's not a joke. It's a deep truth about true nature of reality. As soon as you have a plan it becomes outdated. All other projects tools show a dead picture. You make your plan yesterday according to
  your ideas of yesterday. **A new day has come and it has its own ideas about you :-)**.
  Not your plan will make your day. You cannot predict how the Life will go.
  The Life will tell you by its daily waves of activities. Sometimes it will be related to
  yesterday tasks. Sometimes it will force you to forget everything you have wanted to do today.
  But it is not easy to leave your goals. It is a pain when your plan is ruined.
  Frustration is a shadow of any plan. **Can you be happy if you are in frustration?**
  Nibbana helps your to become a Fenix which is born every day.
  **Nibbana disactivated all your projects every night** and in the morning you have to decide 
  what will make your day.
  After yesterday has passed away and tomorrow came you become more connected to the reality.
  You are new. You have new ideas. You have new priorities.
  Focus on it. Make it your daily **epicenter**. And forget for one day about all other things.
  **Leave it to the care of the Big Mind of the Universe**. 
  Nibbana helps you to focus on your mission. Do your daily project juggling.

* **Limit work in progress**. Nibbana helps you to become honest with yourself.
  It's a total idiotism to take an unbearable burden day by day and cry about your energy,
  healh or broken life. **Do what you can really do**.  You can keep in mind 3-5-7 things
  at the same time. There is no sense in lying yourself you can manage to do this all.
  Be honest and put your mind's limit :-) Mine is 2. Nibbana does not allow me to 
  have more then 2 projects from an area. I just decide what is the project of the day.
  And what I will do if I get stuck on the first project. For me it's enouth :-)

* **All is projects, not tasks** so better create projects not tasks. We used to use 
  projects as conainers for tasks and we operate tasks.
  Usually we create a project, then enter tasks view and start creating tasks.
  But we cannot predict 100%  what steps are required to fullfil the project 
  and our project decomposition (work breakdown structure - WBS) is just a plan.
  If we stick to the plan we could miss another opportunity to reach the project's goal
  as our filters are already set to the WBS defined. So my hint is to define 
  only a few tasks which are really the next ones.
  When you complete these tasks then create the next next tasks according to the new point of the future.
  But better **do not create all WBS tasks at all**.
  So *Nibbana* is built taking the above into consideration. So, create and deal with projects, not tasks.
  **Nibbana gives you a combined list of your projects and tasks** in one view.
  If you define a project task you start to see the task instead of task's project.
  Projects with zero tasks are shown as projects.
  Usually a day shows what is the next task and if you want to keep the chain going (Done metrics)
  just create a task in Done state.

Usage
=====
Some general tips and tricks:

* Use Odoo filters. Create your own filters for Areas.
* Use favorite filters! 

Areas
-----
Area represents a big part of one's life. Usually you'd like to focus on an area and see only projects
from thar area. Area examples:

* Work
* Home
* Sport
* Hobby
* Learning

Limiting work in progress
-------------------------
Each area has active project limit. When this limit is reached you cannot set project to Active state.
You should inactivate one of your currently active projects first. 

Projects
--------
Project states:

* Done
* Active

* Inactive. I don't like to see projects I am not going to work on today.
That's why I move them away as *Inactive* projects. Do not misuse with *Waiting* state. Waiting means
I wait smth from somebody. It's a state. But status is inactive.

* Waiting
* Scheduled
* Cancelled

Tasks
-----
Filters
*******
* Current - shows only tasks from projects in Active state.
* Focus - shows tasks with focus set. Only tasks from active projects are shown.

User preferences
----------------
Daily refocus
*************
Time of deactivation is set in ``[[Settings]] >> Automation >> Scheduled Actions >> Refocus Nibbana projects``
with **Next Execution Date** field.

Now state of all *Active* projects will be set to *Inactive* and user having this feature
enabled will start their day with building project plan for the day.

This feature is enabled by default on per user basis and is located in user's preferences form.

FAQ
===
In Sequential Actions view I cannot click on record, is it a bug of feature?
----------------------------------------------------------------------------
Sequential view is a real PostgreSQL view combining projects and tasks in one dataset.
So depending on where the current record comes from (tasks or projects) a corresponding form
is open. It's hard to hack Odoo to overwrite click-on-record behavior (if you know how to do it get in 
contact pls). As a solution there are icon buttons used to enter record details.

Why Sequential Actions and Unified List views are empty not showing anything?
-----------------------------------------------------------------------------
This is a feature. This is because they are Epicenter showing only Active projects and tasks without 
project in active states (next, today).