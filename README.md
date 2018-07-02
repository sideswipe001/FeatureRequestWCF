Using the web app is fairly self explanatory. Fill in the required fields and drop downs to create a new Feature Request. 
Press the "Submit" button to create the feature request. There is a table at the bottom to show existing Feature Requests
 (for the currently selected client).
There is some basic validation on the inputs - making sure something was provided for the title and description, and that the date field contains a date.


This app is designed to be used in AWS, with Elastic Beanstalk. It utilizes a requirements.txt file to
ensure that all dependencies are being met in the environment, and utilizes several JavaScript libraries,
such as jQuery and KnockoutJS. Bootstrap is used for formatting.

To set it up:

1) Download a copy of this code as a ZIP file.
2) Sign into the AWS management console.
3) Search for Elastic Beanstalk
4) Create a new application, named "Feature Request - WCF", with an optional description.
5) Create a new environment. There is a shortcut that reads "Create one now" in the middle of the page.
6) Choose "Web server environment"
7) Choose a name for the environment, and a domain name; enter them in
8) For Platform, choose "Preconfigured platform" and select Python from the drop down
9) For Application code, choose Upload your code 
10) Select the ZIP file downloaded before, and upload it.
11) Press the "Create Environment" button
12) Wait for the environment creation to complete.
13) Add a database to the environment, by clicking on "Configuration" on the left
14) Find the "Database" section and select "modify"
15) Select "mysql" for the Engine. 
16) Enter a username and password
17) Press "apply"
18) Wait for the DB to finish being created.
19) Edit the configuration to look for app.py, by clicking on "Configuration" on the left
20) In the "Software" section, click "Modify"
21) Change the WSGIPath to app.py
22) Press "Apply" along the bottom.
23) When the environment has finished updating, the Feature Request app should be running properly.


After the app is running, you should be able to load the URL, and be taken to the main page.


Also included are several API endpoints; specifically:

<b>GET</b> endpoints

<i>/api/v1/Client</i>

This endpoint returns a JSON list of Clients from the database.

<i>/api/v1/Area</i>

This endpoint returns a JSON list of Areas from the database.

<i>/api/v1/FeatureRequest</i>

This endpoint returns a JSON list of all submitted Feature Requests.

<i>/api/v1/FeatureRequest/Client/\<id\></i>

This endpoint returns a JSON list of submitted Feature Requests for the provided Client ID.

<b>POST</b> endpoints

<i>/api/v1/FeatureRequest</i>

This endpoint adds a new FeatureRequest to the database. The body of the POST should contain a valid JSON FeatureRequest.
The endpoint will return a 200 with blank text on success.

<i>/api/v1//api/v1/FeatureRequest/\<id\>

This endpoint updates the FeatureRequest with the provided ID. The body of the POST should contain a valid JSON FeatureRequest.
The endpoint will return a 200 with blank text on success.