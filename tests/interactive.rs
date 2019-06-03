mod app {
    use dua::interactive::TreeIndex;
    use dua::{
        interactive::{widgets::SortMode, EntryData, TerminalApp, Tree, TreeIndexType},
        ByteFormat, Color, TraversalSorting, WalkOptions,
    };
    use failure::Error;
    use petgraph::prelude::NodeIndex;
    use pretty_assertions::assert_eq;
    use std::{ffi::OsString, fmt, path::Path};
    use termion::input::TermRead;
    use tui::backend::TestBackend;
    use tui::Terminal;

    const FIXTURE_PATH: &'static str = "tests/fixtures";

    fn debug(item: impl fmt::Debug) -> String {
        format!("{:?}", item)
    }

    #[test]
    fn it_can_handle_ending_traversal_reaching_top_but_skipping_levels() -> Result<(), Error> {
        let (_, app) = initialized_app_and_terminal(&["sample-01"])?;
        let expected_tree = sample_01_tree();

        assert_eq!(
            debug(app.traversal.tree),
            debug(expected_tree),
            "filesystem graph is stable and matches the directory structure"
        );
        Ok(())
    }

    #[test]
    fn it_can_handle_ending_traversal_without_reaching_the_top() -> Result<(), Error> {
        let (_, app) = initialized_app_and_terminal(&["sample-02"])?;
        let expected_tree = sample_02_tree();

        assert_eq!(
            debug(app.traversal.tree),
            debug(expected_tree),
            "filesystem graph is stable and matches the directory structure"
        );
        Ok(())
    }

    #[test]
    fn simple_user_journey() -> Result<(), Error> {
        let long_root = "sample-02/dir";
        let (mut terminal, mut app) = initialized_app_and_terminal(&["sample-02", long_root])?;
        assert_eq!(
            app.state.sorting,
            SortMode::SizeDescending,
            "it starts in descending order by size"
        );

        assert_eq!(
            app.traversal
                .tree
                .node_weight(TreeIndex::new(11))
                .unwrap()
                .name,
            OsString::from(format!("{}/{}", FIXTURE_PATH, long_root)),
            "the roots are always listed with the given (possibly long) names",
        );

        // when hitting the S key
        app.process_events(&mut terminal, b"s".keys())?;
        assert_eq!(
            app.state.sorting,
            SortMode::SizeAscending,
            "it sets the sort to size ascending"
        );

        Ok(())
    }

    fn initialized_app_and_terminal(
        fixture_paths: &[&str],
    ) -> Result<(Terminal<TestBackend>, TerminalApp), Error> {
        let mut terminal = Terminal::new(TestBackend::new(40, 20))?;
        std::env::set_current_dir(Path::new(env!("CARGO_MANIFEST_DIR")))?;

        let input = fixture_paths
            .iter()
            .map(|p| Path::new(FIXTURE_PATH).join(p))
            .collect();
        let app = TerminalApp::initialize(
            &mut terminal,
            WalkOptions {
                threads: 1,
                byte_format: ByteFormat::Metric,
                color: Color::None,
                sorting: TraversalSorting::AlphabeticalByFileName,
            },
            input,
        )?;
        Ok((terminal, app))
    }

    fn sample_01_tree() -> Tree {
        let mut t = Tree::new();
        {
            let mut add_node = make_add_node(&mut t);
            let root_size = 1259070;
            let r = add_node("", root_size, None);
            {
                let s = add_node(
                    format!("{}/{}", FIXTURE_PATH, "sample-01").as_str(),
                    root_size,
                    Some(r),
                );
                {
                    add_node(".hidden.666", 666, Some(s));
                    add_node("a", 256, Some(s));
                    add_node("b.empty", 0, Some(s));
                    add_node("c.lnk", 1, Some(s));
                    let d = add_node("dir", 1258024, Some(s));
                    {
                        add_node("1000bytes", 1000, Some(d));
                        add_node("dir-a.1mb", 1_000_000, Some(d));
                        add_node("dir-a.kb", 1024, Some(d));
                        let e = add_node("empty-dir", 0, Some(d));
                        {
                            add_node(".gitkeep", 0, Some(e));
                        }
                        let sub = add_node("sub", 256_000, Some(d));
                        {
                            add_node("dir-sub-a.256kb", 256_000, Some(sub));
                        }
                    }
                    add_node("z123.b", 123, Some(s));
                }
            }
        }
        t
    }
    fn sample_02_tree() -> Tree {
        let mut t = Tree::new();
        {
            let mut add_node = make_add_node(&mut t);
            let root_size = 1540;
            let r = add_node("", root_size, None);
            {
                let s = add_node(
                    format!("{}/{}", FIXTURE_PATH, "sample-02").as_str(),
                    root_size,
                    Some(r),
                );
                {
                    add_node("a", 256, Some(s));
                    add_node("b", 1, Some(s));
                    let d = add_node("dir", 1283, Some(s));
                    {
                        add_node("c", 257, Some(d));
                        add_node("d", 2, Some(d));
                        let e = add_node("empty-dir", 0, Some(d));
                        {
                            add_node(".gitkeep", 0, Some(e));
                        }
                        let sub = add_node("sub", 1024, Some(d));
                        {
                            add_node("e", 1024, Some(sub));
                        }
                    }
                }
            }
        }
        t
    }

    fn make_add_node<'a>(
        t: &'a mut Tree,
    ) -> impl FnMut(&str, u64, Option<NodeIndex<TreeIndexType>>) -> NodeIndex<TreeIndexType> + 'a
    {
        move |name, size, maybe_from_idx| {
            let n = t.add_node(EntryData {
                name: OsString::from(name),
                size,
                metadata_io_error: false,
            });
            if let Some(from) = maybe_from_idx {
                t.add_edge(from, n, ());
            }
            n
        }
    }

}