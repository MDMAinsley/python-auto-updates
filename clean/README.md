Add the code from application.py in to your main Python application

Setup updater.py & launcher.py and fill in relevant info (github name etc)

Make sure to change names of your main app and the updater to what you need

Make sure to set the correct version number in your main application

Create .exe's of all .py's using pyinstaller

Make sure to name the launcher.exe what you want and style it (This is the main exe to launch your app)

Upload application.exe (or whatever you called it) to github as a latest release, public, and give it a version tag (for example 1.0.0 for the first upload)

Now when you run launcher.exe (or whatever you called it) if the version number in your main app is the same as the tag on github, you should see "No updates" and your program starts

If there is an update, it will download then launch your program