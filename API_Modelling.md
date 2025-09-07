API Modelling :  /api

## User Endpoints
POST /user/google-oauth: Signs in a user/ Creates a new one
POST /user/backup-email: Assigns a backup email to the user
POST /user/set-pr: Sets the role of user to PR (can be accessed by SPOC or admins)
POST /user/set-spoc: Sets the role of user to SPOC (can be accessed by SPOC or admins)
GET /user/profile: Get current user profile
PATCH /user/profile: Update current user profile
GET /user/list: Get list of all users (SPOC/Admin only)
GET /user/{id}: Get user details by ID (SPOC/Admin only)
PATCH /user/{id}: Update user by ID (SPOC/Admin only)
DELETE /user/{id}: Delete user by ID (SPOC/Admin only)
GET /user/roll/{roll_number}: Get user by roll number

## Company Endpoints
GET /company: Gives a list of all the companies
POST /company: Creates a company with required fields
GET /company/{slug}: Fetches the details of that company
PATCH /company/{slug}: Update company details
DELETE /company/{slug}: Deletes company
GET /company/{slug}/experiences: Fetches the experiences of a particular company
GET /company/search: Search companies by name or description
GET /company/analytics: Get company analytics (SPOC/PR/Admin only)

## Experience Endpoints
POST /experience: takes tags list object as body of request, send search results of verified and visible experiences with those tags
POST /experience/create: Takes in required fields and creates an experience
GET /experience/{id}: Fetches the details of that experience
PATCH /experience/{id}: Update experience details
DELETE /experience/{id}: Deletes experience
GET /experience/unverified: Fetches the unverified experiences (accessible by spoc or admin)
GET /experience/self: Get current user's experiences
POST /experience/{id}/save_unsave: Save or unsave an experience
GET /experience/saved: Get user's saved experiences
POST /experience/search: Advanced search experiences with filters
GET /experience/analytics: Get experience analytics (SPOC/PR/Admin only)

## Tag Endpoints
GET /tag: Gives a list of all the tags
POST /tag: Creates a tag with required fields
GET /tag/{id}: Fetches the details of that tag
PATCH /tag/{id}: Update tag details
DELETE /tag/{id}: Deletes tag
GET /tag/search: Search tags by title or type
GET /tag/type: Gives a list of all the tagtypes
POST /tag/type: Creates a tagtype with required fields
GET /tag/type/{id}: Fetches the details of that tagtype
PATCH /tag/type/{id}: Update tagtype details
DELETE /tag/type/{id}: Deletes tagtype
GET /tag/type/{id}/tags: Fetches all tags of the particular tagtype

## Opportunity Endpoints
GET /opportunity/opportunities: Get all opportunities
POST /opportunity/opportunities: Create a new opportunity
GET /opportunity/opportunities/{id}: Get opportunity details
PATCH /opportunity/opportunities/{id}: Update opportunity
DELETE /opportunity/opportunities/{id}: Delete opportunity
POST /opportunity/opportunities/{id}/save: Save an opportunity
POST /opportunity/opportunities/{id}/unsave: Unsave an opportunity
POST /opportunity/opportunities/{id}/verify: Verify an opportunity (SPOC/PR/Admin only)
GET /opportunity/opportunities/saved: Get user's saved opportunities
GET /opportunity/opportunities/analytics: Get opportunity analytics (SPOC/PR/Admin only)

## Notification Endpoints
GET /opportunity/notifications: Get user's notifications
GET /opportunity/notifications/{id}: Get notification details
POST /opportunity/notifications/{id}/mark_read: Mark notification as read
POST /opportunity/notifications/mark_all_read: Mark all notifications as read
DELETE /opportunity/notifications/{id}: Delete notification
POST /opportunity/notifications/create: Create notification (SPOC/PR/Admin only)

## Mentorship Endpoints
GET /opportunity/mentorships: Get user's mentorships
POST /opportunity/mentorships: Create a new mentorship
GET /opportunity/mentorships/{id}: Get mentorship details
PATCH /opportunity/mentorships/{id}: Update mentorship
DELETE /opportunity/mentorships/{id}: Delete mentorship
GET /opportunity/mentorships/available_mentors: Get available mentors

## Analytics Endpoints
GET /analytics/dashboard: Get comprehensive dashboard analytics (SPOC/PR/Admin only)

