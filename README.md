# How to use the app
The purpose of the app is for individual telegram users to record their daily water drinking amount. The app assumes the user is in Hong Kong time 
zone (GMT+8) 

The chatbot have the following commands available: 

/help
- Show instruction of commands 

/add 
- Allow user to add the water amount they drunk. 
- Only allows integers. 
- Accepts minus sign for deducting water amount drunk. 

/check 
- Returns the amount of water drunk recorded by user on that day, the approximate amount in cups (240ml per cup), and gives the percentage of amount drunk is compared to the 
recommendation (8 cups a day) 

/checkpast 
- Allow user to specify the number of past records they want to check. 
- Only allows integers. 

/today 
- command for checking if the date is correct. 
- Returns username (not user id) and date. 
