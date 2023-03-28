import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-portfolio-edit-dialog',
  templateUrl: './portfolio-edit-dialog.component.html',
  styleUrls: ['./portfolio-edit-dialog.component.scss']
})
export class PortfolioEditDialogComponent implements OnInit {

  isLoading: Boolean = true;
  constructor(@Inject(MAT_DIALOG_DATA) public id: number) { }

  ngOnInit(): void {
    this.isLoading = false;
  }

}
