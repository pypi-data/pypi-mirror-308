from argparse import ArgumentParser

from task_maker_brain import TaskManager


def main():

    parser = ArgumentParser(
        prog='TaskManager',
        description='Task Manager for adding, removing and editing tasks on the current project'
    )

    task_manager = TaskManager()

    parser.add_argument('action', choices=['add', 'delete', 'complete', 'read'])
    parser.add_argument('-i', '--id')
    parser.add_argument('-a', '--all', action='store_true')
    parser.add_argument('-t', '--title')
    parser.add_argument('-c', '--completed', action='store_true')

    args = parser.parse_args()

    action = args.action

    match action:

        case 'add':
            try:
                title = args.title
                task_manager.add(title)
            except Exception as e:
                print(e)

        case 'delete':
            title, task_id = args.title, args.id
            if not title and not task_id:
                print('Please provide at least a --title, or an --id')
            if task_id:
                try:
                    task_manager.delete(task_id=task_id)
                except Exception as e:
                    print(e)
            elif title:
                try:
                    task_manager.delete(task_title=title)
                except Exception as e:
                    print(e)

        case 'complete':
            title, task_id = args.title, args.id
            if not title and not task_id:
                print('Please provide at least a --title, or an --id')
            if task_id:
                try:
                    task_manager.complete(task_id=task_id)
                except Exception as e:
                    print(e)
            elif title:
                try:
                    task_manager.complete(task_title=title)
                except Exception as e:
                    print(e)

        case 'read':
            title, task_id, read_all, completed = args.title, args.id, args.all, args.completed
            if not title and not task_id and not read_all:
                print('Please provide at least a --title, an --id, or --all for reading all the existing tasks')
            if read_all:
                try:
                    task_manager.read(read_all=read_all, completed=completed)
                except Exception as e:
                    print(e)
            elif task_id:
                try:
                    task_manager.read(task_id=task_id, completed=completed)
                except Exception as e:
                    print(e)
            elif title:
                try:
                    task_manager.read(task_title=title, completed=completed)
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    main()
