public class GameItem {
    private String name;
    private int price;
    private String description;

    public GameItem(String name, int price, String description) {
        this.name = name;
        this.price = price;
        this.description = description;
    }
    
    // Getters
    public String getName() { return name; }
    public int getPrice() { return price; }
    public String getDescription() { return description; }
}