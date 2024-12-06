# Copyright 2023 BPCells contributors
# 
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# https://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or https://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.


# start delvewheel patch
def _delvewheel_patch_1_9_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'bpcells.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

from .version import __version__
