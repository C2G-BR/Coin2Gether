import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProfilePageComponent } from './profile-page/profile-page.component';
import { ProfileRoutingModule } from './profile-routing.module';
import { MaterialModule } from '../../material.module';
import { FlexLayoutModule } from '@angular/flex-layout';
import { GoogleChartsModule } from 'angular-google-charts';
import { SharedModule } from '../../shared/components/shared.module';
import { EditProfileComponent } from './edit-profile/edit-profile.component';
import { ReactiveFormsModule } from '@angular/forms';
import { PortfolioEditDialogComponent } from './portfolio-edit-dialog/portfolio-edit-dialog.component';

@NgModule({
  declarations: [ProfilePageComponent, PortfolioEditDialogComponent, EditProfileComponent],
  imports: [
    CommonModule,
    MaterialModule,
    ProfileRoutingModule,
    FlexLayoutModule,
    GoogleChartsModule,
    SharedModule,
    ReactiveFormsModule
  ]
})
export class ProfileModule { }
