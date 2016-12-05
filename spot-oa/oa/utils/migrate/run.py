if __name__=='__main__':
    import argparse

    from migration import Migration

    config_file = 'config.json'
    config = Migration.load_config(config_file)

    parser = argparse.ArgumentParser(description='Tool to migrate CSV files')
    parser.add_argument('working_dir', nargs='?', default=config['root'], help="Path to where data is stored")
    args = parser.parse_args()

    config['root'] = args.working_dir

    Migration.run(config)
