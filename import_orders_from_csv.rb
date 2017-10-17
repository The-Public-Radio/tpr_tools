#!/usr/bin/ruby
# Upload kickstarter orders from a CSV to the TPR-Coordinator
# 
# Usage: ruby import_orders_from_csv.rb <path_to_csv> <env> <auth_token> <source>



require 'CSV'
require 'httparty'

# set arguments
backers_csv = CSV.read(ARGV[0])
env = ARGV[1]
auth_token = ARGV[2]
source = ARGV[3]


case env
when 'production'
	url='https://api.thepublicrad.io/orders'
when 'staging'
	url='https://api-staging.thepublicrad.io/orders'
end


 
# Import CSV

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
	  name: name,
	  order_source: source,
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
	headers = {'Authorization' => "Bearer #{auth_token}", 'Content-Type' => 'application/json'}
	puts url  
  	response = HTTParty.post(url, headers: headers, body: order_params.to_json)

  if (200..299).include?(response.code)
  	puts 'Success!'
  else
  	puts "An error occured uplading order #{order_params}: #{response.body}"
  end
end;nil