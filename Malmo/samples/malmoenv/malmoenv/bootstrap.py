# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------
import os
import subprocess
import pathlib


def download(branch=None, build=True, installdir="MalmoPlatform", version="0.36.0"):
    """Download Malmo from github and build (by default) the Minecraft Mod.
       Example usage: import malmoenv.bootstrap; malmoenv.bootstrap.download()
    Args:
        branch: optional branch to clone. TODO Default is release version.
        build: build the Mod unless build arg is given as False.
        installdir: the install dir name. Defaults to MalmoPlatform.
        version: the malmo version. Testing only.
    Returns:
        The path for the Malmo Minecraft mod.
    """
    gradlew = './gradlew'
    if os.name == 'nt':
        gradlew = 'gradlew.bat'

    if branch is None:
        branch = "malmoenv"  # TODO change to release version i.e. branch = version

    cwd = os.getcwd()
    subprocess.check_call(["git", "clone", "-b", branch, "https://github.com/Microsoft/malmo.git", installdir])
    os.chdir(installdir)
    os.chdir("Minecraft")
    try:
        # Create the version properties file.
        pathlib.Path("src/main/resources/version.properties").write_text("malmomod.version={}\n".format(version))
        # Optionally do a test build.
        if build:
            subprocess.check_call([gradlew, "setupDecompWorkspace", "build", "testClasses",
                                   "-x", "test", "--stacktrace", "-Pversion={}".format(version)])
        minecraft_dir = os.getcwd()
    finally:
        os.chdir(cwd)
    return minecraft_dir


def launchMinecraft(port, installdir="MalmoPlatform", replaceable=False):
    """Launch Minecraft listening for malmoenv connections.
    Args:
        port - the TCP port to listen on.
        installdir: the install dir name. Defaults to MalmoPlatform.
        Must be same as given (or defaulted) in download call if used.
        replaceable: whether or not to automatically restart Minecraft (default is false).
    """
    launch_script = 'launchClient.sh'
    if os.name == 'nt':
        launch_script = 'launchClient.bat'
    cwd = os.getcwd()
    try:
        os.chdir(installdir)
        os.chdir("Minecraft")
        cmd = [launch_script, '-port', str(port),'-env']
        if replaceable:
            cmd.append('-replaceable')
    finally:
        subprocess.check_call(cmd)
        os.chdir(cwd)
