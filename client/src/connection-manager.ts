

export class ConnectionManager {
    
    private static destination: string = 'http://localhost:8000'

    
    public static predictRoute(data: any, callback: (res: any) => any) {
        const { destination } = ConnectionManager;
        fetch(`${destination}/predict-route`, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
        })
            .then(res => res.json())
            .then(res => callback(res))
            .catch(e => console.log(e));
    }    

    public static checkConnection(callback: (res: any) => any) {
        const { destination } = ConnectionManager;

        fetch(`${destination}/check-connection`, {
            method: 'GET'
        })
            .then(res => res.json())
            .then(res => callback(res))
            .catch(e => console.log(e));
    }

}