from rich.console import Console

def show_menu():
    c=Console()
    items=['Scan all drives','Scan one drive','Scan selected folder','Search files','View detected projects','View protected folders','Generate reports','Build move plan','Review move plan','Execute approved move plan','Rollback previous move batch','Exit']
    c.print('\n[bold]File Organizer Menu[/bold]')
    for i, it in enumerate(items, start=1):
        c.print(f'{i}. {it}')
