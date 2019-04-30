import java.io.File;

public class FileDoesNotExistException extends Exception {
    private String message = null;

    public FileDoesNotExistException() {
        super();
    }

    public FileDoesNotExistException(String message) {
        super(message);
        this.message = message;
    }

    public FileDoesNotExistException(Throwable cause){
        super(cause);
    }

    @Override
    public String toString(){
        return message;
    }

    @Override
    public String getMessage() {
        return message;
    }
}
