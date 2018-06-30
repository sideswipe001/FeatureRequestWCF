function AppViewModel() {
    this.title = ko.observable();
    this.description = ko.observable();
}

ko.applyBindings(new AppViewModel());