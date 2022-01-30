# Google-Scraper
### This Project Scrapes Google for a Search Query and Stores the results in a Google Spreadsheet
#### It has an Elegant and Clean UI developed in Bootstrap Studio and the backend is written in Django

### Some Screenshots of its working:

![image](https://user-images.githubusercontent.com/53652715/151703753-7d58ad36-398e-4dbb-8493-e1f3c6b71699.png)

![image](https://user-images.githubusercontent.com/53652715/151703768-7936a3c3-5119-415b-8653-14a4d3442a50.png)

### Results of Scraping:

![image](https://user-images.githubusercontent.com/53652715/151703834-cccc2937-42c6-490d-aa3e-c12fb54da3ec.png)

### Logs:

![image](https://user-images.githubusercontent.com/53652715/151703810-c4af8035-f221-4cc5-b0b0-af41cfeaa55b.png)

### How to Run: 

First, extract the ZIP files in a folder, let's call it **main**.

#### You will need a Google service account json credentials file for authorization in pygshees: 
1. Head to [Google Developers Console](https://console.developers.google.com/) and create a new project (or select the one you have.)

  ![image](https://user-images.githubusercontent.com/53652715/150808514-67c3791a-7716-4998-8adc-8078e561dc49.png)
  
2. You will be redirected to the Project Dashboard, there click on “Enable Apis and services”, search for “Sheets API”.
  
  ![image](https://user-images.githubusercontent.com/53652715/150809142-7c62d195-577c-4bb2-b423-282efb8bda07.png)

3. In the API screen click on ‘ENABLE’ to enable this API.
  
  ![image](https://user-images.githubusercontent.com/53652715/150809095-4d6e1a91-9971-494f-93a5-f8972716a8b4.png)

4. Similarly enable the “Drive API”. We require drives api for getting list of spreadsheets, deleting them etc.
5. Go to Sheets API screen, then go to “Credentials” tab and choose “Create Credentials > Service Account Key”.
6. Next choose the service account as ‘App Engine default’ and Key type as JSON and click create:
  
  ![image](https://user-images.githubusercontent.com/53652715/150808998-feb2dbde-e24e-4bf9-96e3-c3f64a1578a3.png)

7. You will now be prompted to download a .json file. This file contains the necessary private key for account authorization. Name the file as **'service_account_sheets.json'**. 

  ![image](https://user-images.githubusercontent.com/53652715/150808866-2c170cc8-de90-460b-801e-ea53ebe5ae00.png)

This is how this file may look like:
>{
>    "type": "service_account",
>    "project_id": "p....sdf",
>    "private_key_id": "48.....",
>    "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
>    "client_email": "p.....@appspot.gserviceaccount.com",
>    "client_id": "10.....454",
>}

8. After getting the json file, paste it in the *main* folder. 

Now, to install all the dependencies:
1. Open the *main* folder in the terminal. 
2. Write this command:
> pip install -r requirements.txt
3. After all dependencies are installed successfully, run the server:
> python manage.py runserver
4. Now, you will get a link in the terminal, open that in a browser. 
