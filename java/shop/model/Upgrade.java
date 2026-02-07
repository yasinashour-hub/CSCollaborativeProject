package shop.model; 
// !!THIS FILE IS DONE. DO NOT CODE ANYMORE HERE. 
// shop/model/ is where we will put the data and rules, not stuff w/ screens/clicks 
// shop/model/Upgrade.java is where the idea of the upgrades will be eg. cost, effect, name, description, etc. 
public class Upgrade { 
    // data for the upgrades 
    private String name; 
    private int cost; 
    private String description; 
    private int bonusAmount; 
    // obvious 
    public Upgrade(String name, int cost, String description, int bonusAmount) { 
        this.name = name; 
        this.cost = cost; 
        this.description = description; 
        this.bonusAmount = bonusAmount; 
        } 
    // getters for the data 
    public String getName() { 
        return name; 
    } 
    public int getCost() { 
        return cost; 
    } 
    public String getDescription() { 
        return description; 
    } 
    public int getBonusAmount() { 
        return bonusAmount; 
    } 
}