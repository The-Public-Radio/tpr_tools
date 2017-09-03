#! /bin/bash

heroku pg:reset -a tpr-coordinator-staging --confirm tpr-coordinator-staging
sleep 5
heroku run rake db:migrate -a tpr-coordinator-staging
sleep 5
heroku run rake db:seed -a tpr-coordinator-staging
