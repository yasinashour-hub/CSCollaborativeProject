package shop.logic; 
import shop.model.Upgrade;
// !!shop/logic is for rules and flow, not visuals 
// !!shop/logic/ShopInventory is for what upgrades the shop sells, has a list, methods to see what stuff we have, 
// contd... stuff for out of stock, tiers, and maybe sales 
// Item list: tiered shoes that give more speed, one-time use potions that give temp stat buffs for all of our stats,
// tiered rackets that give more power, different tennis balls to choose that increase diff stats,
// a water bottle to increase a stamina stat for a match
// and anything else you think of
public class ShopInventory { 
    public static void main(String[] args) { 
        Upgrade shoes = new Upgrade( "Basic Tennis Shoes", 10, "Increases your base speed by 1.", 1);
        System.out.println(shoes.getName()); 
        System.out.println(shoes.getCost()); 
        System.out.println(shoes.getDescription()); 
        System.out.println(shoes.getBonusAmount()); 
    } 
}