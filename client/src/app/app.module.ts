import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import '@angular/localize/init';
import { LayoutModule } from '@angular/cdk/layout';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { MaterialModule } from './material.module';
import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { SidenavComponent } from './template/sidenav/sidenav.component';

import { HttpErrorInterceptor } from './shared/interceptors/http-error.interceptor';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { SharedModule } from './shared/components/shared.module';

import {IvyCarouselModule} from 'angular-responsive-carousel';

import { HashLocationStrategy, LocationStrategy } from '@angular/common';

@NgModule({
  declarations: [AppComponent, SidenavComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LayoutModule,
    MaterialModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    SharedModule,
    IvyCarouselModule,
    // HashLocationStrategy,
    // LocationStrategy
  ],
  providers: [{provide: LocationStrategy, useClass: HashLocationStrategy}],
  // providers: [{ provide: HTTP_INTERCEPTORS, useClass: HttpErrorInterceptor, multi: true }],
  bootstrap: [AppComponent],
})
export class AppModule {}
