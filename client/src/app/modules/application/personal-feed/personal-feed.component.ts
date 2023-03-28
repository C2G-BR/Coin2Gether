import { Component, OnInit } from '@angular/core';
import { zip } from 'rxjs';
import { BlogPostService } from '../../../shared/services/blog-post/blog-post.service';
import { TradeService } from '../../../shared/services/trade/trade.service';
import { Trade } from '../../../shared/models/trade.model';
import { BlogPost } from '../../../shared/models/blog-post.model';
import { User } from '../../../shared/models/user.model';
import { RecommenderService } from 'src/app/shared/services/recommender/recommender.service';

@Component({
  selector: 'app-personal-feed',
  templateUrl: './personal-feed.component.html',
  styleUrls: ['./personal-feed.component.scss']
})
export class PersonalFeedComponent implements OnInit {

  feedList: (BlogPost | Trade)[] = [];
  userList: any[] = [];

  constructor(
    private blogPostService: BlogPostService, 
    private tradeService: TradeService,
    private RecommenderService: RecommenderService
  ) { }


  ngOnInit(): void {
    zip(
      this.RecommenderService.getRecommenders(),
      this.tradeService.getAllFollowedTrades(),
      this.blogPostService.getAllFollowedPosts()
    ).subscribe(([users, trades, blogPosts]: [any, Trade[], BlogPost[]]) => {
      this.userList = users["data"];
      console.log(this.userList);
      this.feedList = blogPosts;
      this.feedList = this.feedList.concat(trades);
      this.sortByDate(this.feedList);
    });
  }

  private sortByDate(feed: (BlogPost | Trade)[]) {
    feed.sort((a, b) => {
      if (a.date != undefined && b.date != undefined) {
        return (a.date > b.date) ? -1 : 1
      } else return -1;
    });
  }

}
