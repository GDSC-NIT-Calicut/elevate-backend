Creating Tags
{
    "title":"",
    "type_id": int
}


creating experiences
{
   
    cover_image= models.ImageField(upload_to='experience_images/',null=True,blank=True)
   
    title = models.CharField(max_length=200)
   
    role = models.CharField(max_length=100)
   
    short_description = models.TextField()
   
    content = models.TextField()
   
    experience_date = date
   
    visibility=boolean default true
   
    job_type='placement', 'internship', 'research, or 'other' (all other inputs will give a  bad response)
   
    company = get a dropdwon of companies let them choose

    tag_ids=integer array of tag ids
}

Keep in mind giving the tag body as 'tag_ids' and company body as 'company_id' when requesting from experience endpoints and       type body as'type_id' when requesting tag endpoints 

Do not give it as 'tags' and 'type' and 'company'