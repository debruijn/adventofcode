use pyo3::pyfunction;

// 2018 day 14, utility function in Rust
#[pyfunction]
pub fn find_recipe<'a>(input: usize) -> (Vec<usize>, usize) {

    // part 1 in its own namespace
    let part1 = {
        let mut recipes = vec![3, 7];
        let mut p1 = 0;
        let mut p2 = 1;
        let nr_take = 10;
        while recipes.len() < input + nr_take {
            let mut score = recipes[p1] + recipes[p2];

            // Push to recipes for one digit at a time
            if score >= 10 {
                recipes.push(score / 10);
                score %= 10;
            }
            recipes.push(score);

            // New p
            p1 = (p1 + 1 + recipes[p1]) % recipes.len();
            p2 = (p2 + 1 + recipes[p2]) % recipes.len();
        }
        recipes[input..input+nr_take].to_vec()
    };

    // part 2 - can immediately return when answer found
    let mut recipes = vec![3, 7];
    let mut p1 = 0;
    let mut p2 = 1;
    // input as vector in this case
    let input: Vec<usize> = input.to_string().chars().map(|d|
        d.to_digit(10).unwrap() as usize).collect();
    let ans;
    loop {
        let mut score = recipes[p1] + recipes[p2];
        let mut two_digit = false;
        if score >= 10 {
            two_digit = true;
            recipes.push(score / 10);
            score %= 10;
        }
        recipes.push(score);
        p1 = (p1 + 1 + recipes[p1]) % recipes.len();
        p2 = (p2 + 1 + recipes[p2]) % recipes.len();

        let recipe_len = recipes.len();
        let input_len = input.len();
        if recipe_len > input_len {  // can only check when recipe is long enough
            if &recipes[recipe_len - input_len..recipe_len] == input {
                ans = recipe_len - input_len;  // match final il digits
                return (part1, ans);
            }
        }
        if two_digit && recipe_len > input_len + 1 { // different ending possible for two_digit case
            if &recipes[recipe_len - 1 - input_len..recipe_len - 1] == input {
                ans = recipe_len - 1 - input_len;
                return (part1, ans);
            }
        }
    }
}