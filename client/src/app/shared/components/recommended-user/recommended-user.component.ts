import { Component, OnInit, Input } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-recommended-user',
  templateUrl: './recommended-user.component.html',
  styleUrls: ['./recommended-user.component.scss']
})

export class RecommendedUserComponent implements OnInit {

  @Input() userList: any = [];

  constructor(
      public authService: AuthService,
  ) { }

  ngOnInit(): void {
  }

}
