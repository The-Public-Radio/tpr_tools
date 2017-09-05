#!/usr/bin/ruby
# Upload kickstarter orders from a CSV to the TPR-Coordinator
# 
# Usage: python import_orders_from_csv.py <path_to_csv>
require 'CSV'
require 'httparty'
 
# Import CSV
backers_csv = CSV.read(ARGV[0])
headers = backers_csv.shift

backer_list = []

backers_csv.each do |backer|
	hash = {}
	headers.each_with_index do |header,i|
		hash[header] = backer[i]
	end
	backer_list << hash
end

backer_list.each do |backer|
	if !backer['Shipping Name'].nil?
		name = backer['Shipping Name']
	else
		name = backer['Backer Name']
	end

	order_params = {
	  first_name: name.split(' ')[0],
	  last_name: name.split(' ')[1],
	  order_source: "kickstarter",
	  email: backer['Email'],
	  street_address_1: backer['Shipping Address 1'],
	  street_address_2: backer['Shipping Address 2'],
	  city: backer['Shipping City'],
	  state: backer['Shipping State'],
	  postal_code: backer['Shipping Postal Code'],
	  country: backer['Shipping Country Code'],
	  phone: backer['Shipping Phone Number']
	}

	frequencies = []

	backer.select{ |s| s.include?('Radio') }.each do |k,v|
		frequencies << v
	end

	order_params['frequencies'] = { backer['Shipping Country Code']  => frequencies.compact }

	# Post to TPR Coordinator
	url = 'http://api-staging.thepublicrad.io/orders'
	headers = {'Content-Type' => 'application/json'}
  
  response = HTTParty.post(url, headers: headers, body: order_params.to_json)

  puts response.code
end;nil