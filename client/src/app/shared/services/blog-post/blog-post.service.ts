import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, retry } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { BlogPost } from '../../models/blog-post.model';
import { AuthService } from '../auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class BlogPostService {

  constructor(private httpClient: HttpClient, private authService: AuthService) { }

  BLOG_POST_ENDPOINT = 'blogs';

  public getAllPosts(): Observable<BlogPost[]> {
    return this.httpClient.get(environment.apiEndpoint + this.BLOG_POST_ENDPOINT + '/').pipe(
      retry(2),
      map((data: any) => {
        return data.data.filter((post: BlogPost) => {
          return this.isBlogPost(this.parseToBlogPost(post));
        }
        );
      })
    );
  }

  public getAllFollowedPosts(): Observable<BlogPost[]> {
    let options = this.authService.getOptions();
    return this.httpClient.get(environment.apiEndpoint + this.BLOG_POST_ENDPOINT + "/followed", options=options).pipe(
      retry(2),
      map((data: any) => {
        return data.data.filter((post: BlogPost) => {
          return this.isBlogPost(this.parseToBlogPost(post));
        }
        );
      })
    );
  }

  public getPostsByAuthor(author: String): Observable<BlogPost[]> {
    let options = this.authService.getOptions();
    return this.httpClient.get(environment.apiEndpoint + this.BLOG_POST_ENDPOINT + '/' + author, options=options).pipe(
      retry(2),
      map((data: any) => {
        return data.data.filter((post: BlogPost) => {
          return this.isBlogPost(this.parseToBlogPost(post));
        }
        );
      })
    );
  }

  public getPostById(id: number): Observable<BlogPost> {
    return this.httpClient.get(environment.apiEndpoint + this.BLOG_POST_ENDPOINT + '/' + id.toString()).pipe(
      retry(2),
      map((data: any) => {
        return this.parseToBlogPost(data.data);
      })
    );
  }

  private parseToDate(dateString: any): Date {
    let date = new Date(dateString);
    date = date ? date : new Date();
    return date;
  }

  private parseToBlogPost(data: any): BlogPost {
    data.interface = "blog-post";
    data.date = this.parseToDate(data.date);
    return data;
  }

  private isBlogPost(blogPost: BlogPost): Boolean {
    try {
      if (!isNaN(this.parseToDate(blogPost.date).getTime())) {
        return true
      } else {
        return false;
      }
    } catch (error) {
      return false
    }
  }
}
