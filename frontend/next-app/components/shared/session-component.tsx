// Any component in your application
import { useApi } from "./session-context";

function MyComponent() {
    const api = useApi(); // Access the api object

    console.log(api)

    // Now you can use api methods or properties as needed
    // For example: api.someMethod()

    return (
        <div>
            {/* Render your component */}
        </div>
    );
}

export default MyComponent;
