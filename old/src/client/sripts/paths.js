class Paths {
    static MAIN = 'http://127.0.0.1:5500/';
    static BACKUPS = Paths.MAIN + 'backups/';
    static QUERIES = Paths.MAIN + 'queries/';
    static TEMP = Paths.MAIN + 'temp/';
    static CONFIG = Paths.MAIN + 'config/';
    static SOURCE = Paths.MAIN + 'src/';
    static CLIENT = Paths.SOURCE + 'client/';
    static SERVER = Paths.SOURCE + 'server/';
    static ASSETS = Paths.CLIENT + 'assets/';
    static SCRIPTS = Paths.CLIENT + 'scripts/';
    static STYLES = Paths.CLIENT + 'styles/';
    static TEMPLATES = Paths.CLIENT + 'templates/';
}

export { Paths };
