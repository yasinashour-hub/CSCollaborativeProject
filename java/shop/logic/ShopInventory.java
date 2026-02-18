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
    
    private Upgrade shoes;
    private Upgrade racket;
    private Upgrade speedPotion;
    private Upgrade powerPotion;
    private Upgrade spinBall;
    private Upgrade pointBall;
    private Upgrade waterBottle;

    public ShopInventory() {

        // Shoes upgrade
        shoes = new Upgrade(
            "Basic Tennis Shoes",              
            10,                                
            "Increases your base speed by 1.", 
            "speed",                           
            1,                                 
            false,                            
            false,
            true                             
        );
        
        // Racket upgrade
        racket = new Upgrade(
            "Basic Racket", 
            10, 
            "Increases your base power by 1.", 
            "power",
            1,
            false,
            false,
            true
        );

        // Potions
        speedPotion = new Upgrade(
            "Speed Potion I", 
            3, 
            "Increases your speed by 5% for the next match.", 
            "speed",
            1.05,
            true,
            true,
            false
        );

        powerPotion = new Upgrade(
            "Power Potion I", 
            3, 
            "Increases your power by 5% for the next match.", 
            "power",
            1.05,
            true,
            true,
            false
        );


        // Tennis Ball Upgrades

        spinBall = new Upgrade(
                "Spin Ball", 
                5, 
                "Increases your spin by 5% when using this ball.", 
                "spin",
                1.05,
                true,
                false,
                true
        );

        pointBall = new Upgrade(
            "Score Ball",
            5, 
            "Gives you one extra point at the start of the match when using this ball.",
            "score",
            1,
            false,
            false,
            true
        );

        // Water Bottle Upgrade

        waterBottle = new Upgrade(
            "Basic Water Bottle",
            4,
            "Increases your base stamina by 1.",
            "stamina",
            1,
            false,
            false,
            true
        );
    }

    public Upgrade getShoes() {
            return shoes;
    }

    public Upgrade getRacket() {
            return racket;
    }

    public Upgrade getSpeedPotion() {
            return speedPotion;
    }

    public Upgrade getPowerPotion() {
            return powerPotion;
    }

    public Upgrade getSpinBall() {
            return spinBall;
    }

    public Upgrade getPointBall() {
            return pointBall;
    }

    public Upgrade getWaterBottle() {
            return waterBottle;
    }
     
}
