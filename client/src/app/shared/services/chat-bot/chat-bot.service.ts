import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map, retry } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { AuthService } from '../auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class ChatBotService {

  constructor(private httpClient: HttpClient, private authService: AuthService) { }

  public postMessage(message:string | null, session_id:string | null): Observable<any> {
    let headers:HttpHeaders;

    if (this.authService.isAuthenticated()) {
      const token = this.authService.getToken();
      headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': token
      });
    } else {
      headers = new HttpHeaders({
        'Content-Type': 'application/json'
      });
    }

    let options = { headers: headers };

    const obj: Object = {
      message: message,
      session_id: session_id
    }

    return this.httpClient.post(environment.apiEndpoint + 'chatbot/', obj, options).pipe(
      retry(2),
      map((data: any) => {
        console.log(data)
        return data
      })
    );
  }
}
