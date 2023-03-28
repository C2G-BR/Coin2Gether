import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map, retry } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { AuthService } from '../auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class RecommenderService {

  constructor(private httpClient: HttpClient, private authService: AuthService) { }

  public getRecommenders() {

    let options = this.authService.getOptions();

    return this.httpClient.get(environment.apiEndpoint + 'recommender/', options=options).pipe(
      retry(2),
      map((data2: any) => {
        return data2
      })
    );

  }

  
}
