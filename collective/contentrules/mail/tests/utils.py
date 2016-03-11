# -*- coding: utf-8 -*-
# Copyright (c) 2008 Ingeniweb

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Generic Test case for collective.contentrules.mail doctest
"""
__docformat__ = 'restructuredtext'

from DateTime import DateTime


def addMember(self, username, fullname="", email="", roles=('Member', ), last_login_time=None):
    """Create an new member

    The password is always 'secret'
    """
    self.portal.portal_membership.addMember(username, 'secret', roles, [])
    member = self.portal.portal_membership.getMemberById(username)
    member.setMemberProperties({'fullname': fullname, 'email': email,
                                'last_login_time': DateTime(last_login_time)})


def setUpDefaultMembers(self):
    """Setup default members"""

    addMember(self, 'manager1', 'Manager one', roles=('Manager', 'Member'))
    addMember(self, 'manager2', 'Manager two', roles=('Manager', 'Member'))
    addMember(self, 'reviewer1', 'Reviewer one', roles=('Reviewer', 'Member'))
    addMember(self, 'reviewer2', 'Reviewer two', roles=('Reviewer', 'Member'))
    addMember(self, 'member1', 'Member one', roles=('Member', ))
    addMember(self, 'member2', 'Member two', roles=('Member', ))
    addMember(self, 'authenticated1', 'Authenticated one', roles=('Anonymous', ))
    addMember(self, 'anonymous1', 'Anonymous one', roles=('Anonymous', ))
