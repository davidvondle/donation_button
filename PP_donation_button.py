import mechanize
import boto3
import os

sns=boto3.client('sns')
phone_number='+13128675309'
kms = boto3.client('kms', region_name='us-west-2')

from base64 import b64decode
CC_number=kms.decrypt(CiphertextBlob=b64decode(os.environ['CC_number']))['Plaintext']
CC_expiration_month= kms.decrypt(CiphertextBlob=b64decode(os.environ['CC_expiration_month']))['Plaintext']
CC_expiration_year= kms.decrypt(CiphertextBlob=b64decode(os.environ['CC_expiration_year']))['Plaintext']
CC_CSC=kms.decrypt(CiphertextBlob=b64decode(os.environ['CC_CSC']))['Plaintext']

br = mechanize.Browser(factory=mechanize.RobustFactory()) 

def lambda_handler(event, context):
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	br.open("https://secure.ppaction.org/site/Donation2?df_id=12913&12913.donation=form1")
	br.select_form(name="process")

	br.form['gift_type']=["onetime",] 
	br.form['level_standardexpanded']=["30882",] 
	br.form['level_standardexpanded30882amount']="5"
	br.form['billing_first_namename']="FIRSTNAME"
	br.form['billing_last_namename']="LASTNAME"
	br.form['billing_addr_street1name']="ADDRESS"
	br.form['billing_addr_street2name']=""
	br.form['billing_addr_cityname']="CITY"
	br.form['billing_addr_state']=["IL",] #2 letter code
	br.form['billing_addr_zipname']="90210"
	br.form['billing_addr_country']=["United States",]
	br.form['donor_email_addressname']="name@email.com"

	br.form['responsive_payment_typecc_numbername']=CC_number
	br.form['responsive_payment_typecc_exp_date_MONTH']=[CC_expiration_month] #1-12
	br.form['responsive_payment_typecc_exp_date_YEAR']=[CC_expiration_year] #4 digit
	br.form['responsive_payment_typecc_cvvname']=CC_CSC

	response = br.submit()

	if "Thank you" in response.read():
		message = '$5 donated to Planned Parenthood!'
		sns.publish(PhoneNumber=phone_number, Message=message)
	else:
		message = 'Error: no donation occurred'
		sns.publish(PhoneNumber=phone_number, Message=message)
