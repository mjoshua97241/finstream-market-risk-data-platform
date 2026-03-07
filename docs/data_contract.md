# Sample (To be override once confirmed)
Market Data Contract

Source: Yahoo Finance API

Expected fields:
symbol (string)
timestamp (datetime)
open (float)
high (float)
low (float)
close (float)
volume (integer)

Update frequency:
Hourly

Validation rules:
no null symbol
volume >= 0
timestamp must be unique per symbol