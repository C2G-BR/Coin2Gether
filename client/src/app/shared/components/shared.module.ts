import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FeedComponent } from '../../shared/components/feed/feed.component';
import { MaterialModule } from '../../material.module';
import { BlogPostComponent } from '../../shared/components/blog-post/blog-post.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { BlogDialogComponent } from './blog-dialog/blog-dialog.component';
import { TradeComponent } from './trade/trade.component';
import { TradeDialogComponent } from './trade-dialog/trade-dialog.component';
import { RouterModule } from '@angular/router';
import { EditPortfolioComponent } from './edit-portfolio/edit-portfolio.component';
import { ChatBotComponent } from './chat-bot/chat-bot.component';
import { RecommendedUserComponent } from './recommended-user/recommended-user.component';
import {IvyCarouselModule} from 'angular-responsive-carousel';

@NgModule({
  declarations: [FeedComponent, BlogPostComponent, BlogDialogComponent, TradeComponent, TradeDialogComponent, EditPortfolioComponent, ChatBotComponent, RecommendedUserComponent],
  imports: [
    CommonModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    RouterModule,
    IvyCarouselModule,
  ],
  exports: [
    FeedComponent,
    EditPortfolioComponent,
    ChatBotComponent,
    RecommendedUserComponent
  ]
})
export class SharedModule { }
