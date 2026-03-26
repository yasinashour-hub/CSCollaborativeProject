# CSCollaborativeProject
This project is comprised of two different parts: the shop and the main game.
The main game is a python file names tennis. The shop was built in java with an intricate architecture. Since java is a class-based language, it is conventional and professional to have all unique tasks or structures in their own files. These can easily come togeather to talk to each other as so: ShopScreen --> Shop --> ShopInventory --> Upgrade.
In java, there is shop, which has the stuff for the main shop, and shopgames, where we could the shop games for a tiny bit more money if we have time
The instructions for each of the folders (assets, logic, model, ui) in shop, are in the first files of each one, and each file has its own directions at the top.
But since assets can't have any written files in it, the instructions are in here:
Assets is for NON-CODE FILES ONLY. I put one in python as well. It should ONLY have images (background images, button images, icons, title screen, etc.).
The shop SHOULD work like this, if a player clicks buy on a better racket, ShopScreen.java will be where they will do that, and it will trigger the Shop.java logic to see if they can buy it, and if they can it will subtract the money. Then the ShopInventory.java will give the player the thing they asked for (the data source) and then Upgrade.java will say exactly what it does. 
Now we just have to code it...
