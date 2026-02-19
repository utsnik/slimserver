@echo off
plink -batch -pw Oxford31. utking@10.1.4.12 "id && docker --version"
