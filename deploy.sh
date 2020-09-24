#!/bin/bash
sudo systemctl restart nginx
sudo systemctl restart portfolio.service
if [ -f .env ]
then
  export $(cat .env | xargs)
fi
sleep 1
sudo systemctl status nginx
sudo systemctl status portfolio

