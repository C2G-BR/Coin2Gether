import { Component, Inject, OnInit } from '@angular/core';
import { Validators, UntypedFormGroup, UntypedFormBuilder, UntypedFormArray, AbstractControl, FormControl, ValidatorFn } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { DOCUMENT } from '@angular/common';
import { AuthService } from '../../../shared/services/auth/auth.service';
import { MustMatch } from '../../../shared/validators/must-match.validator';
import { UserService } from '../../../shared/services/user/user.service';
import { User, UserUpdate } from '../../../shared/models/user.model';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.scss']
})
export class EditProfileComponent implements OnInit {

  
  public hide1 = true;
  public hide2 = true;
  minDate = new Date();
  maxDate = new Date();
  public socialMediaPlatforms: string[] = ["Facebook", "Instagram", "Twitter", "LinkedIn", "TikTok"];
  public user: User = {
    username: "Username",
    email: "email@gmail.com",
    firstName: "Firstname",
    lastName: "Lastname",
    country: "Country",
    password: "Qwertz1234314!!",
    birthdate: new Date(),
    zip: 2324234
  };

  public signupForm: UntypedFormGroup = this.formBuilder.group({
    firstName: [this.user?.firstName, Validators.required],
    lastName: [this.user?.lastName, Validators.required],
    birthdate: [this.user?.birthdate, Validators.required],
    accounts: this.formBuilder.array([])
  });
  

  constructor(
    private authService: AuthService,
    private _snackBar: MatSnackBar,
    private router: Router,
    private formBuilder: UntypedFormBuilder,
    private userService: UserService,
    private dialogRef: MatDialogRef<EditProfileComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    @Inject(DOCUMENT) private _document: Document,
    private httpClient: HttpClient,
  ) {
    this.maxDate.setFullYear(this.minDate.getFullYear() - 18);
    this.minDate.setFullYear(this.minDate.getFullYear() - 120); 
  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 2000,
    });
  }

  simpleAccounts() {
    return this.signupForm.get("accounts");
  }

  accounts(): UntypedFormArray {
    return this.signupForm.get("accounts") as UntypedFormArray
  }

  appendNewAccount(platform:string, username:string) {
    let acc = this.newAccount();
    acc.patchValue({
      socialMediaPlatform: platform,
      username: username
    });
    this.accounts().push(acc);
  }

  newAccount(): UntypedFormGroup {
    return this.formBuilder.group({
      socialMediaPlatform:  [null, Validators.required],
      username:  [null, Validators.required]
    })
  }

  addAccount() {
    this.getAccounts();
    this.accounts().push(this.newAccount());
  }

  getAccounts() {
    return this.signupForm.value.accounts;
  }

  removeAccount(indexAcc:number) {
    this.accounts().removeAt(indexAcc);
  }

  ngOnInit() {
    let headers;
    try {
      const token = this.authService.getToken();
      headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': token
      });
    }catch {
      headers = new HttpHeaders({
        'Content-Type': 'application/json',
      });
    }

    let options = { headers: headers };
    this.httpClient.get(environment.apiEndpoint + 'user/update', options).subscribe((result: any) => {
      try {
        this.signupForm.patchValue({
          birthdate : result.birthdate,
          firstName : result.firstName,
          lastName : result.lastName
        });

        for (let acc of result.account) {
          this.appendNewAccount(acc.socialMediaPlatform, acc.socialMediaAccount);
        }
      } catch {
        this._snackBar.open('Error. There are some troubles with loading the users. Please try again!', 'Close');
      }
    }, error => {
      this._snackBar.open('Error. There are some troubles with reaching the server. Please contact our Admin!', 'Close');
    });
  }


  public close() {
    this.dialogRef.close(this.signupForm.value);
  }

  public save() {
    let user: UserUpdate = {
      firstName: this.signupForm.value.firstName,
      lastName: this.signupForm.value.lastName,
      birthdate: this.signupForm.value.birthdate,
      account: this.signupForm.value.accounts
    };
    let headers;
    try {
      const token = this.authService.getToken();
      headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': token
      });
    }catch {
      headers = new HttpHeaders({
        'Content-Type': 'application/json',
      });
    }
    let options = { headers: headers };
    this.httpClient.post(environment.apiEndpoint + 'user/update', user, options).subscribe((result: any) => {
      this.dialogRef.close();
      this._document.defaultView?.location.reload();
    }, error => {
      this._snackBar.open('Error. There are some troubles with reaching the server. Please contact our Admin!', 'Close');
    });
  }
}
