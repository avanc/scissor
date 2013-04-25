# Copyright (C) 2013 Sven Klomp (mail@klomp.eu)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

class WrongFileTypeError(Exception):
    """Exception raised for wrong filetype.

    Attributes:
        filename -- filename of wrong type
        expected -- Expected file type
    """

    def __init__(self, filename, expected):
        self.filename = filename
        self.expected = expected
        
    def __str__(self):
        return "Got '{0}' but expected '*{1}'.".format(self.filename, self.expected)
