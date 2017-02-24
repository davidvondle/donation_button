# donation_button
This Python script is built upon [this quick-and-dirty solution] https://github.com/nathanpryor/donation_button to build an Amazon Dash button that would donate to Planned Parenthood through the page https://secure.ppaction.org/site/Donation2?df_id=12913&12913.donation=form1

The script requires the Mechanize library (http://wwwsearch.sourceforge.net/mechanize/).

Replace the obvious placeholders with your own information. 

It's set up to be run on Amazon's AWS Lambda service, with the credit card info stored as the following encrypted environment variables for a tiny bit more security:
	CC_number
	CC_expiration_month
	CC_expiration_year
	CC_CSC
If you're not doing that, go ahead and put them in as strings.

See the file country_and_state_codes.txt for the exact state and country syntax.

An Illustrator file is also attached with art and a cut path separated into layers to produce your own sticker.