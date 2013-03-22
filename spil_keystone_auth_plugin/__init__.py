# Copyright (c) 2012 Spil Games
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

try:
    with open('VERSION') as f:
        version = __version__ = f.read().strip()
except:
    print "could not read version file"
    version_info = (0 , 0, 0)
    version = __version__ = ".".join(map(str, version_info))