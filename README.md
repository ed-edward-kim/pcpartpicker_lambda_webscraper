# pcpartpicker_lambda_webscraper
This allows you to webscrap a products price from PcPartPicker, sending an email whenever the selected product goes below your set price target. Using AWS Lamda, this application can be ran even when your computer is off! Using a csv file, we can select the products we want, what price it needs to be to send an email to us, and the link to the product. 

In order to use this, you must first make an AWS account. Add the files and deploy the zip however you like. This should show up under the "Functions" tab. For me, I linked my Visual Studio Code with AWS lamda such that I can build and deploy it using 'sam build --use-container' and 'sam deploy --guided', following the instructions.

If you follow the same steps as me, make sure that you choose the right server for AWS Lambda, as it will not show the project. To see your server, you can click the state next to your username at the top right of AWS. This should show which server you are on such as us-east-2 and so on. 

Once you upload the project to AWS, you must make one more change. Within the app.py python file, you need to change line 25 and 26, putting your email and password inbetween the quotes for sender and password. This is so that you can email yourself. I recommend making an new email for this, such that it does not spam you and will only have the contents of the products you want. 

Lastly, we need to add a trigger such that the app can refresh every hour. To do this, we go to the functions page and click on the "Add trigger". We will add an EventBridge(CloudWatch Events), and set it such that it has a rate of 1 hour by typing in rate(1 hour). You can make this interval shorter, however this triggers the websites DDos protection and may block you out. In my testing, 1 hour works great and does not block you out, however this may depend on how many products are on your list.
