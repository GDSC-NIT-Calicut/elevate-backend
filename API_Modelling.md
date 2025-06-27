API Modelling :  /api

GET /company: Gives a list of all the companies

POST/company: Creates a company with required fields

GET/company/id: Fetches the details of that company

PATCH/company/id: Update company details

DELETE/company/id: Deletes company



POST /experience : takes tags list object as body of request, send search results of experiences with those tags, 

POST/experience/create: Takes in required fields and creates an experience

GET/experience/id: Fetches the details of that experience

PATCH/experience/id: Update experience details

DELETE/experience/id: Deletes experience



GET /tag/type: Gives a list of all the tagtypes

POST/tag/type: Creates a tagtype with required fields

GET/tag/type/id: Fetches the details of that tagtype

PATCH/tag/type/id: Update tagtype details

DELETE/tag/type/id: Deletes tagtype



GET /tag: Gives a list of all the tags

POST/tag: Creates a tag with required fields

GET/tag/id: Fetches the details of that tag

PATCH/tag/id: Update tag details

DELETE/tag/id: Deletes tag



POST /user/google-oauth: Signs in a user/ Creates a new one

POST/backup-email: Assigns a backup email to the user

