import java.lang.reflect.Field;
import java.util.ArrayList;

public class Utils {

    public Utils(){
        ;
    }

    public static Object cloneObject(Object obj){
        try{
            Object clone = obj.getClass().newInstance();
            for (Field field : obj.getClass().getDeclaredFields()) {
                field.setAccessible(true);
                field.set(clone, field.get(obj));
            }
            return clone;
        }catch(Exception e){
            return null;
        }
    }

    public static ArrayList<Integer> range(int low, int high){
        ArrayList<Integer> numbers = new ArrayList<>();
        for (int i=low; i<high; i++){
            numbers.add(i);
        }
        return numbers;
    }
}
