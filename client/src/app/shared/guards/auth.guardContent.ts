import { CanActivate, Router } from '@angular/router';
import { Injectable } from '@angular/core';
import { AuthService } from '../services/auth/auth.service';


@Injectable({
    providedIn: 'root'
})
export class AuthGuardContent implements CanActivate {

    constructor(
        private router: Router,
        private authService: AuthService
    ) { }


    public canActivate(): boolean {
        if (!this.authService.isAuthenticated()) {
            return true;
        } else {
            try {
                const username = this.authService.getUsername();
                this.router.navigate(['profile/' + username]);
                return false;
            }
            catch {
                return true;
            }
        }
    }

}
