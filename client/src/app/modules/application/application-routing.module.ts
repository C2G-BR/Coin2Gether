import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AnonymousGuard } from 'src/app/shared/guards/anonymous.guard';
import { AuthGuard } from 'src/app/shared/guards/auth.guard';
import { AuthGuardContent } from 'src/app/shared/guards/auth.guardContent';
import { NewsFeedComponent } from './news-feed/news-feed.component';
import { PersonalFeedComponent } from './personal-feed/personal-feed.component';

const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('../landing/landing.module')
      .then(m => m.LandingModule),
    canActivate: [AuthGuardContent]
  },
  {
    path: 'blog',
    loadChildren: () => import('../blog/blog.module')
      .then(m => m.BlogModule)
  },
  {
    path: 'auth',
    loadChildren: () => import('../auth/auth.module')
      .then(m => m.AuthModule),
    canActivate: [AnonymousGuard],
  },
  {
    path: 'trade',
    loadChildren: () => import('../trade/trade.module')
      .then(m => m.TradeModule),
    canActivate: [AuthGuard],
  },
  {
    path: 'about',
    loadChildren: () => import('../about/about.module')
      .then(m => m.AboutModule)
  },
  {
    path: 'profile/:username',
    loadChildren: () => import('../profile/profile.module')
      .then(m => m.ProfileModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'feed',
    component: NewsFeedComponent
  },
  {
    path: 'feed/personal',
    component: PersonalFeedComponent,
    canActivate: [AuthGuard]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ApplicationRoutingModule { }
