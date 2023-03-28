import { Component, OnInit, ViewChild, ElementRef, ChangeDetectorRef } from '@angular/core';
import { Validators, UntypedFormGroup, UntypedFormBuilder } from '@angular/forms';
import { ChatBotService } from 'src/app/shared/services/chat-bot/chat-bot.service';
import { AuthService } from 'src/app/shared/services/auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-chat-bot',
  templateUrl: './chat-bot.component.html',
  styleUrls: ['./chat-bot.component.scss']
})

export class ChatBotComponent implements OnInit {

  messages: Array<{ title: string, tag: string }> = [];
  sessionId: string | null = null;
  isConfirmation: boolean = false;

  @ViewChild('cb-send-input') sendbox!: ElementRef; 

  constructor(
    private router: Router,
    private formBuilder: UntypedFormBuilder,
    private chatbotService: ChatBotService,
    private authService: AuthService,
    private ref: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.sendMessage(null);
    if (typeof this.sendbox !== 'undefined') {
      this.sendbox.nativeElement.focus();
    }
  }

  public messageForm: UntypedFormGroup = this.formBuilder.group({
    message: [null, Validators.required]
  }); 

  public cancelSession(): void {
    this.sessionId = null;
    this.answer("I cancelled the session. Ask me something new.");
  }

  public submit(): void {
    const new_message = this.messageForm.value.message;
    this.messages.push({title: new_message, tag: "user"});
    this.ref.detectChanges();
    this.messageForm.reset();
    this.sendMessage(new_message);
  }

  public sendConfirmation(): void {
    this.isConfirmation = false;
    this.sendMessage('true');
  }

  public sendDisconfirmation(): void {
    this.isConfirmation = false;
    this.sendMessage('false');
  }

  private sendMessage(message:string | null): void {
    this.chatbotService.postMessage(message, this.sessionId).subscribe(result => {
      this.sessionId = result['session_id'];
      if (result['is_action']) {
        this.switch_action(result['message']);
      } else if (result['is_confirmation']) {
        this.isConfirmation = true;
        this.answer(result['message']);
      } else {
        this.answer(result['message']);
      }
    });
  }

  private switch_action(action:string): void {
    action = action.split('::')[1]
    switch (action) {
      case "logout":
        this.authService.logout();
        this.router.navigate(['']);
        break;
      case "profile":
        if (this.authService.isAuthenticated()) {
          this.router.navigate(['/profile', this.authService.getUsername()]);
        } else {
          this.router.navigate(['/auth']);
        }
        break;
      case "homepage":
        this.router.navigate(['/']);
        break;
      case "personal_feed":
        this.router.navigate(['/feed/personal']);
        break;
      case "public_feed":
        this.router.navigate(['/feed/']);
        break;
      case "auth":
        if (this.authService.isAuthenticated()) {
          this.router.navigate(['/profile', this.authService.getUsername()]);
          this.answer("You are already logged in. I navigated you to your profile page.");
        } else {
          this.router.navigate(['/auth']);
        }
        break;
      case "create_post":
        if (this.authService.isAuthenticated()) {
          this.router.navigate(['/blog/post']);
        } else {
          this.router.navigate(['/auth']);
          this.answer("You aren't logged in. I navigated you to the login page. Please login first and try again.");
        }
        break;
      case "create_trade":
        if (this.authService.isAuthenticated()) {
          this.router.navigate(['/trade/newTrade']);
        } else {
          this.router.navigate(['/auth']);
          this.answer("You aren't logged in. I navigated you to the login page. Please login first and try again.");
        }
        break;
      default:
        this.answer("The action could not be performed.");
    }
  }

  private answer(message:string): void {
    var counter = this.messages.push({title: "", tag: "loading"});
    this.ref.detectChanges();
    setTimeout( () => {this.push_answer(message, counter) }, 1000 + (Math.random() * 20) * 100);
  }

  private push_answer(message:string, counter:number): void {
    this.messages[counter-1] = {title: message, tag: "bot"};
    if (typeof this.sendbox !== 'undefined') {
      this.sendbox.nativeElement.focus();
    }
    this.ref.detectChanges();
  }
}
