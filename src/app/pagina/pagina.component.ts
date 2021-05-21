import { Component, OnInit } from '@angular/core';
import {AngularFireDatabase, AngularFireList} from "@angular/fire/database";
import {Observable} from "rxjs";
import { AngularFirestore } from '@angular/fire/firestore';
@Component({
  selector: 'app-pagina',
  templateUrl: './pagina.component.html',
  styleUrls: ['./pagina.component.css']
})
export class PaginaComponent implements OnInit {

  messages: AngularFireList<any>;

  constructor(private db: AngularFireDatabase,private store:AngularFirestore) {
    this.messages = this.db.list('/pictures');
    const doc = this.store.collection('pictures').get();

    const sub = doc.subscribe((snapshot) => {
      const page = snapshot.forEach(pas =>{
        console.log(pas);
      });
    })
    console.log(doc);
  }

  getMessages(): Observable<any> {
    this.messages = this.db.list('/pictures');
    return this.messages.valueChanges();
  }

ngOnInit() {
  this.messages = this.db.list('/pictures');
  console.log(this.messages);

}

}
