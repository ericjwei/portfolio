#!/bin/bash
export PORTFOLIO_SETTINGS="settings.cfg"
sudo systemctl restart nginx
sudo systemctl restart portfolio.service
sleep 2
sudo systemctl status nginx
sudo systemctl status portfolio
