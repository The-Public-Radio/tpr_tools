
# A sketch of pulling backer country data and formatting the radio presets, which are 
# needed in addition to the frenquency  
# BAND, Deemphasis, and Channel spacing are arguments that are passed to eeprom.py 
# in the form of: eeprom.py -f $frequency -b $band -d $deemphasis -s $channel_spacing
# Hong Kong, New Zeland, Israel, Faroe Islands 

EU = ['BE', 'BG', 'CZ', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'HR',
 'IT', 'CY', 'LV', 'LT', 'LU', 'HU', 'MT', 'NL', 'AT', 'PL', 
 'PT', 'RO', 'SI', 'SK', 'FI', 'SE', 'UK', 'GB', 'DK', 'CH']

# Need to add South America
Americas = ['US', 'CA','AI','AG','AW','BS','BB','BZ','BM',
'VG','CA','KY','CR','CU','CW','DM','DO','SV','GL','GD','GP','GT',
'HT','HN','JM','MQ','MX','PM','MS','CW','KN','NI','PA','PR','KN','LC',
'PM','VC','TT','TC','VI','SX','BQ','SA','SE', 'AR', 'BO', 'BR','CL',
'CO','EC','FK','GF','GY','PY','PE','SR','UY','VE']

Asia = ['AF','AM','AZ','BH','BD','BT','BN','KH','CN','CX','CC','IO',
'GE','HK','IN','ID','IR','IQ','IL','JO','KZ','KP','KR','KW','KG',
'LA','LB','MO','MY','MV','MN','MM','NP','OM','PK','PH','QA','SA','SG','LK',
'SY','TW','TJ','TH','TR','TM','AE','UZ','VN','YE','PS']

def get_preset(country):

	if country in EU:
		band = 0
		deemphasis = 1
		channel_spacing = 1
		region = 'EU'

	elif country in Asia:
		band = 0
		deemphasis = 1
		channel_spacing = 1
		region = 'Asia'

	elif country == 'AU':
		band = 0
		deemphasis = 1
		channel_spacing = 0
		region = 'Australia'

	elif country == 'JP':
		band = 1
		deemphasis = 1
		channel_spacing = 1
		region = 'Japan'

	else:
		band = 0
		deemphasis = 0
		channel_spacing = 0
		region = 'Americas'
	
	print "STATUS: Shipping to %s in region %s" % (country, region)
	print "        Band: %d" % band
	print "        Deemphasis: %d" % deemphasis
	print "        Ch. Spacing: %d" % channel_spacing

	return { 'band': str(band), 'deemphasis': str(deemphasis), 'channel_spacing': str(channel_spacing) }


get_preset('BE')
