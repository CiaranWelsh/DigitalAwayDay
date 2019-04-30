import org.junit.Test;

public class RandomCollectionTests {

    public void RandomCollection(){
        ;
    }

    @Test
    public void test1() {
        RandomCollection<Object> rc = new RandomCollection<>()
                .add(40, "dog").add(35, "cat").add(25, "horse");

        for (int i = 0; i < 10; i++) {
            System.out.println(rc.next());
        }
    }
}
